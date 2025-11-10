import { NextRequest, NextResponse } from "next/server";

// Force dynamic rendering for this API route
export const dynamic = 'force-dynamic';
import { promises as fs } from 'fs';
import path from 'path';
// Load data files dynamically to avoid import issues
async function loadCandidatesData(): Promise<CandidatesData> {
  const filePath = path.join(process.cwd(), 'data', 'candidates.json');
  const fileContents = await fs.readFile(filePath, 'utf8');
  return JSON.parse(fileContents) as CandidatesData;
}

async function loadCouncilMembersData(): Promise<CouncilMembersData> {
  const filePath = path.join(process.cwd(), 'data', 'council_members.json');
  const fileContents = await fs.readFile(filePath, 'utf8');
  return JSON.parse(fileContents) as CouncilMembersData;
}
import pointInPolygon from "@turf/boolean-point-in-polygon";
import distance from "@turf/distance";
import center from "@turf/center";
import { point } from "@turf/helpers";
import type { Feature, Polygon, MultiPolygon, FeatureCollection } from "geojson";
import { booleanPointInPolygon } from '@turf/turf';
import { Candidate, CouncilMember } from '@/types/types';

// Type definitions for our data files
interface CandidatesData {
  candidates: Candidate[];
}

interface CouncilMembersData {
  members: CouncilMember[];
}

interface DistrictProperties {
  name: string;
  district: string;
  description?: string;
  representative?: string;
}

// Data will be loaded dynamically in the functions

// Chattanooga bounds - expanded to be more inclusive
const CHATTANOOGA_BOUNDS = {
  north: 35.2200, // Northern boundary (expanded)
  south: 34.9500, // Southern boundary (expanded)
  east: -85.1200, // Eastern boundary (expanded)
  west: -85.4000  // Western boundary (expanded)
};

// Cache the boundaries in memory
let detailedBoundariesCache: FeatureCollection | null = null;
let simplifiedBoundariesCache: FeatureCollection | null = null;
let lastCacheTime: number = 0;
const CACHE_DURATION = 1000 * 60 * 60; // 1 hour

// Helper function to check if coordinates are within Chattanooga bounds
function isWithinChattanooga(lat: number, lon: number): boolean {
  return (
    lat >= CHATTANOOGA_BOUNDS.south &&
    lat <= CHATTANOOGA_BOUNDS.north &&
    lon >= CHATTANOOGA_BOUNDS.west &&
    lon <= CHATTANOOGA_BOUNDS.east
  );
}

// Helper function to create district response object
async function createDistrictResponse(
  district: Feature<Polygon | MultiPolygon, any>,
  source: string,
  isApproximate: boolean = false
) {
  // Get district number, trying multiple property formats from GeoJSON
  const rawDistrictNumber = district.properties?.citydst || 
                           district.properties?.district || 
                           district.properties?.name?.replace('District ', '') || 
                           "Unknown";
  
  // Convert district number to string without decimal (8.0 -> 8)
  const districtNumber = rawDistrictNumber.toString().includes('.') ? 
                        Math.floor(parseFloat(rawDistrictNumber)).toString() : 
                        rawDistrictNumber.toString();
  
  const districtDescription = district.properties.description || 
                             `City Council District ${districtNumber}`;
  
  // Load data asynchronously
  const candidatesData = await loadCandidatesData();
  const councilMembersData = await loadCouncilMembersData();
  
  // Find candidates for this district
  const districtCandidates = (candidatesData.candidates || [])
    .filter((c: Candidate) => c.district === districtNumber)
    .map((c: Candidate) => c.name);
  
  // Find current council member for this district
  const councilMember = councilMembersData.members?.find(
    (m: CouncilMember) => m.district === districtNumber
  );
  
  return {
    district_number: districtNumber,
    district_description: districtDescription,
    precinct: `District ${districtNumber} Precinct - Contact Hamilton County Election Commission at (423) 209-6300 for specific precinct details`,
    polling_place: "Early voting locations and Election Day polling places available at Hamilton County Election Commission",
    polling_address: "Visit https://elect.hamiltontn.gov/ or call (423) 209-6300 for your specific polling location based on your address",
    candidates: districtCandidates,
    council_member: councilMember?.name || district.properties.representative || "Position Vacant",
    council_contact: councilMember?.contact || "(423) 643-7100",
    council_email: councilMember?.email || `district${districtNumber}@chattanooga.gov`,
    council_member_status: councilMember?.status || "vacant",
    council_member_note: councilMember?.note || null,
    source: source,
    is_approximate: isApproximate
  };
}

// Helper function to load district boundaries
async function loadDistrictBoundaries(simplified: boolean = false): Promise<FeatureCollection> {
  const now = Date.now();
  
  // Check if cache is still valid
  if (simplified && simplifiedBoundariesCache && now - lastCacheTime < CACHE_DURATION) {
    return simplifiedBoundariesCache;
  }
  if (!simplified && detailedBoundariesCache && now - lastCacheTime < CACHE_DURATION) {
    return detailedBoundariesCache;
  }

  // Load the GeoJSON file from data directory
  const filePath = path.join(process.cwd(), 'data', 'Current City Council Districts_20250331.geojson');
  const fileContents = await fs.readFile(filePath, 'utf8');
  const boundaries = JSON.parse(fileContents) as FeatureCollection;

  // Update cache
  if (simplified) {
    simplifiedBoundariesCache = boundaries;
  } else {
    detailedBoundariesCache = boundaries;
  }
  lastCacheTime = now;

  return boundaries;
}

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const lat = searchParams.get('lat');
    const lng = searchParams.get('lng');
    const simplified = searchParams.get('simplified') === 'true';

    // If coordinates provided, use detailed boundaries for accuracy
    if (lat && lng) {
      const latitude = parseFloat(lat);
      const longitude = parseFloat(lng);

      // Validate coordinates
      if (isNaN(latitude) || isNaN(longitude)) {
        return NextResponse.json({ error: 'Invalid coordinates' }, { status: 400 });
      }

      // Check if coordinates are within reasonable bounds for Chattanooga
      if (latitude < 34.5 || latitude > 35.5 || longitude < -85.5 || longitude > -84.5) {
        return NextResponse.json({ 
          error: 'Location is outside of Chattanooga city limits',
          errorType: 'OUT_OF_BOUNDS',
          details: 'This location appears to be outside the Chattanooga city limits. Please verify your address or location is within the city limits and try again.'
        }, { status: 400 });
      }

      const boundaries = await loadDistrictBoundaries(false); // Always use detailed for point lookup
      const pt = point([longitude, latitude]);

      for (const feature of boundaries.features) {
        const districtFeature = feature as Feature<Polygon | MultiPolygon>;
        if (booleanPointInPolygon(pt, districtFeature)) {
          // Create the full district response using the helper function
          const districtResponse = await createDistrictResponse(districtFeature, 'GeoJSON District Boundaries');
          
          return NextResponse.json(districtResponse, {
            headers: {
              'Cache-Control': 'public, max-age=3600', // 1 hour
              'Vary': 'Accept-Encoding'
            }
          });
        }
      }

      return NextResponse.json({ 
        error: 'Location is outside of Chattanooga city limits',
        errorType: 'NOT_IN_DISTRICT',
        details: 'This location could not be matched to any City Council district. Please verify your address is within Chattanooga city limits and try again.'
      }, { status: 404 });
    }

    // If no coordinates, return full boundaries (simplified or detailed)
    const boundaries = await loadDistrictBoundaries(simplified);
    
    return NextResponse.json(boundaries, {
      headers: {
        'Cache-Control': 'public, max-age=3600', // 1 hour
        'Vary': 'Accept-Encoding'
      }
    });

  } catch (error) {
    console.error('Error in district API:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
} 