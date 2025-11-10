import { NextRequest, NextResponse } from "next/server";

// Force dynamic rendering for this API route
export const dynamic = 'force-dynamic';

// Known addresses in Chattanooga for more reliable geocoding
const knownAddresses: Record<string, [number, number]> = {
  "101 E 11th St, Chattanooga, TN 37402": [35.0442, -85.3077], // City Hall
  "1001 Lindsay St, Chattanooga, TN 37402": [35.0470, -85.3081], // Library
  "1221 Mississippi Ave, Chattanooga, TN 37405": [35.0456, -85.3097], // Mississippi Ave
  "727 E 11th St, Chattanooga, TN 37403": [35.0433, -85.2993], // Community Kitchen
  "736 Market St, Chattanooga, TN 37402": [35.0465, -85.3089], // Miller Plaza
};

// Chattanooga ZIP code validation
const CHATTANOOGA_ZIP_CODES = new Set([
  '37401', '37402', '37403', '37404', '37405', '37406', 
  '37407', '37408', '37409', '37410', '37411', '37412', 
  '37415', '37416', '37419', '37421', '37450', '37351'
]);

// Chattanooga bounds check - more precise for North Chattanooga area
const CHATTANOOGA_BOUNDS = {
  north: 35.0924, // Northern boundary - adjusted for North Chattanooga
  south: 34.9824, // Southern boundary
  east: -85.1555, // Eastern boundary
  west: -85.3724  // Western boundary
};

// Helper function to check if coordinates are within Chattanooga bounds
function isWithinChattanooga(lat: number, lon: number): boolean {
  return (
    lat >= CHATTANOOGA_BOUNDS.south &&
    lat <= CHATTANOOGA_BOUNDS.north &&
    lon >= CHATTANOOGA_BOUNDS.west &&
    lon <= CHATTANOOGA_BOUNDS.east
  );
}

// Extracts street address from the query
function extractStreet(query: string): string {
  // Remove zip code pattern if present
  return query.replace(/,?\s+\d{5}(?:-\d{4})?$/, '').trim();
}

// Extracts zip code from the query
function extractZipCode(query: string): string | null {
  const zipMatch = query.match(/\b\d{5}(?:-\d{4})?\b/);
  return zipMatch ? zipMatch[0] : null;
}

// Normalize an address for comparison
function normalizeAddress(address: string): string {
  const normalized = address.toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/[^\w\s]/g, '')
    .trim();
  console.log('Address normalization:', {
    original: address,
    normalized: normalized
  });
  return normalized;
}

// Check if the input address matches any known address (fuzzy match)
function findKnownAddress(query: string): [number, number] | null {
  const normalizedQuery = normalizeAddress(query);
  
  // Log the normalized query for debugging
  console.log('Normalized query:', normalizedQuery);
  
  // Check for exact match first
  for (const [address, coords] of Object.entries(knownAddresses)) {
    if (normalizeAddress(address) === normalizedQuery) {
      console.log('Found exact match for known address:', address);
      return coords;
    }
  }
  
  // Check for partial matches (address starts with query or query contains significant portions of address)
  for (const [address, coords] of Object.entries(knownAddresses)) {
    const normalizedAddress = normalizeAddress(address);
    
    // If the address contains the entire query
    if (normalizedAddress.includes(normalizedQuery)) {
      console.log('Found partial match for known address:', address);
      return coords;
    }
    
    // If the query contains significant parts of the address
    const addressParts = normalizedAddress.split(' ');
    const queryParts = normalizedQuery.split(' ');
    
    // Check if all significant address parts (street number, name) are in the query
    const significantParts = addressParts.slice(0, 3); // First 3 parts are usually most important
    const matchesSignificantParts = significantParts.every(part => 
      part.length > 2 && queryParts.some(qPart => qPart.includes(part) || part.includes(qPart))
    );
    
    if (matchesSignificantParts) {
      console.log('Found significant parts match for known address:', address);
      return coords;
    }
  }
  
  return null;
}

// Helper function to validate address components
function validateAddressComponents(data: any): boolean {
  if (!data || !data.address) return false;
  
  const addr = data.address;
  
  // Check if we have a house number and street
  if (!addr.house_number || !addr.road) {
    console.log("Missing house number or street:", addr);
    return false;
  }
  
  // Verify it's in Chattanooga
  if (addr.city?.toLowerCase() !== 'chattanooga' && 
      addr.town?.toLowerCase() !== 'chattanooga') {
    console.log("Not in Chattanooga:", addr);
    return false;
  }
  
  // Verify state is TN
  if (addr.state !== 'Tennessee' && addr.state !== 'TN') {
    console.log("Not in Tennessee:", addr);
    return false;
  }
  
  return true;
}

// Helper function to format coordinates consistently
function formatCoordinates(lat: string | number, lon: string | number): [number, number] {
  // Convert to numbers and fix precision to 6 decimal places
  const formattedLat = parseFloat(parseFloat(lat.toString()).toFixed(6));
  const formattedLon = parseFloat(parseFloat(lon.toString()).toFixed(6));
  
  // Log the formatting
  console.log("Formatting coordinates:", { original: [lat, lon], formatted: [formattedLat, formattedLon] });
  
  return [formattedLat, formattedLon];
}

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get("q");

    if (!query) {
      return NextResponse.json(
        { error: "Query parameter 'q' is required" },
        { status: 400 }
      );
    }

    console.log("\n=== Starting Geocoding Process ===");
    console.log("Original query:", query);

    // Extract ZIP code from the query
    const zipMatch = query.match(/\b\d{5}\b/);
    const zipCode = zipMatch ? zipMatch[0] : null;
    console.log("Extracted ZIP code:", zipCode);

    // Validate ZIP code is in Chattanooga
    if (zipCode && !CHATTANOOGA_ZIP_CODES.has(zipCode)) {
      console.log("❌ Invalid ZIP code:", zipCode);
      return NextResponse.json(
        { error: "The provided ZIP code is not within Chattanooga city limits." },
        { status: 400 }
      );
    }

    // First check if this is a known address
    const normalizedQuery = normalizeAddress(query);
    console.log("\nChecking known addresses for:", normalizedQuery);
    
    for (const [address, coords] of Object.entries(knownAddresses)) {
      const normalizedAddress = normalizeAddress(address);
      console.log("\nComparing with known address:", {
        address: address,
        normalized: normalizedAddress,
        coords: coords,
        matches: {
          exactMatch: normalizedAddress === normalizedQuery,
          addressIncludesQuery: normalizedAddress.includes(normalizedQuery),
          queryIncludesStreet: normalizedQuery.includes(normalizeAddress(address.split(',')[0]))
        }
      });
      
      if (normalizedAddress.includes(normalizedQuery) || 
          normalizedQuery.includes(normalizeAddress(address.split(',')[0]))) {
        console.log("✓ Found matching known address:", {
          address: address,
          coords: coords,
          matchType: normalizedAddress.includes(normalizedQuery) ? 'address includes query' : 'query includes street'
        });
        return NextResponse.json({
          lat: coords[0],
          lon: coords[1],
          display_name: address,
          source: "Known Address Database",
          precision: "high"
        });
      }
    }

    // Try OpenStreetMap Nominatim with specific formatting for Chattanooga
    const nominatimFormats = [
      `${query}, Chattanooga, Tennessee, United States`,
      `${query}, Chattanooga, TN ${zipCode || ''}`.trim(),
      query
    ];

    console.log("\nTrying Nominatim with formats:", nominatimFormats);

    for (const format of nominatimFormats) {
      try {
        console.log("\nTrying format:", format);
        const nominatimUrl = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(format)}&format=json&addressdetails=1&limit=1&countrycodes=us`;
        console.log("Nominatim URL:", nominatimUrl);
        
        const response = await fetch(nominatimUrl, {
          headers: {
            "User-Agent": "ChattanoogaElectionApp/1.0",
          },
        });

        if (!response.ok) {
          console.log(`❌ Nominatim response not OK for format "${format}"`, response.status);
          continue;
        }

        const data = await response.json();
        console.log("Nominatim response:", data);

        if (data && data.length > 0) {
          const lat = parseFloat(data[0].lat);
          const lon = parseFloat(data[0].lon);
          
          console.log("Checking coordinates:", {
            lat,
            lon,
            isWithinBounds: isWithinChattanooga(lat, lon)
          });
          
          if (isWithinChattanooga(lat, lon)) {
            console.log("✓ Found valid location:", {
              lat,
              lon,
              format,
              display_name: data[0].display_name
            });
            return NextResponse.json({
              lat,
              lon,
              display_name: data[0].display_name,
              address_components: data[0].address,
              source: "OpenStreetMap",
              precision: "high"
            });
          } else {
            console.log("❌ Location outside Chattanooga bounds");
          }
        } else {
          console.log("❌ No results from Nominatim");
        }
      } catch (error) {
        console.error(`Error with Nominatim format "${format}":`, error);
      }
    }

    console.log("\n❌ No valid location found");
    return NextResponse.json(
      { error: "Could not find a valid location in Chattanooga for this address." },
      { status: 404 }
    );
  } catch (error) {
    console.error("Geocoding error:", error);
    return NextResponse.json(
      { error: "Failed to geocode the address" },
      { status: 500 }
    );
  }
} 