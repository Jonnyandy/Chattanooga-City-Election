import { Candidate } from "../types/types";

// Types matching your Python app
export type DistrictBoundary = {
  type: "Feature";
  properties: {
    district: string;
    description: string;
    demographics?: Record<string, any>;
  };
  geometry: {
    type: string;
    coordinates: number[][][];
  };
};

export type CouncilMember = {
  name: string;
  district: string;
};

export type PollingPlace = {
  name: string;
  address: string;
  precinct: string;
};

export type DistrictInfo = {
  district_number: string;
  district_description?: string;
  precinct: string;
  polling_place: string;
  polling_address: string;
  distance: string;
  candidates: string[];
  council_member?: CouncilMember;
  error?: string;
};

// A mapping of district numbers to their boundaries
export type DistrictBoundaries = Record<string, DistrictBoundary>;

/**
 * Get district boundaries - in a real app, this would load from a database or GeoJSON file
 */
export async function getDistrictBoundaries(): Promise<DistrictBoundaries> {
  // Simplified for this example - in a real app you'd load from a file or database
  const districts: DistrictBoundaries = {};
  
  // Create mock boundaries for 9 districts
  for (let i = 1; i <= 9; i++) {
    const district = String(i);
    
    // Generate a simple polygon for visualization
    // In a real app, these would be actual district boundaries
    const centers: Record<number, [number, number]> = {
      1: [-85.35, 35.11],
      2: [-85.24, 35.14],
      3: [-85.24, 35.16],
      4: [-85.09, 35.07],
      5: [-85.23, 35.07],
      6: [-85.23, 35.01],
      7: [-85.33, 35.02],
      8: [-85.22, 35.09],
      9: [-85.23, 35.07]
    };
    
    const center = centers[i] || [-85.25, 35.10]; // Default center if not found
    const size = 0.03;
    
    districts[district] = {
      type: "Feature",
      properties: {
        district: district,
        description: `District ${district}`
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [center[0] - size, center[1] - size],
            [center[0] + size, center[1] - size],
            [center[0] + size, center[1] + size],
            [center[0] - size, center[1] + size],
            [center[0] - size, center[1] - size]
          ]
        ]
      }
    };
  }
  
  return districts;
}

/**
 * Determine which district a point is in
 */
export function getDistrictForCoordinates(lat: number, lon: number): string | "District not found" {
  // In a real app, this would use proper geometric point-in-polygon algorithms
  // For this example, we'll use a simplified approach
  
  // For demonstration, just pick a random district
  // In a real app, you would check which polygon contains the point
  const randomDistrict = Math.floor(Math.random() * 9) + 1;
  return String(randomDistrict);
}

/**
 * Get information about a council member
 */
export function getCouncilMember(district: string): CouncilMember {
  // Mock data based on your CSV file
  const councilMembers: Record<string, string> = {
    "1": "Chip Henderson",
    "2": "Jenny Hill",
    "3": "Ken Smith",
    "4": "Darrin Ledford",
    "5": "Carol Berz",
    "6": "Raquetta Dotley",
    "7": "Marvene Noel",
    "8": "Anthony Byrd",
    "9": "Demetrus Coonrod"
  };
  
  return {
    name: councilMembers[district] || "Information unavailable",
    district
  };
}

/**
 * Get candidates for a district
 */
export function getDistrictCandidates(district: string): string[] {
  // Mock data based on your Python files
  const candidates: Record<string, string[]> = {
    "1": ["Chip Henderson", "James \"Skip\" Burnette"],
    "2": ["Jenny Hill"],
    "3": ["Jeff Davis", "Tom Marshall"],
    "4": ["Cody Harvey"],
    "5": ["Dennis Clark", "Cory Hall", "Isiah (Ike) Hester", "Samantha Reid-Hawkins"],
    "6": ["Jenni Berz", "Jennifer Gregory", "Mark Holland", "Christian Siler", "Robert C Wilson"],
    "7": ["Raquetta Dotley"],
    "8": ["Anna Golladay", "Marvene Noel", "Doll Sandridge", "Kelvin Scott"],
    "9": ["Ron Elliott", "Letechia Ellis", "Evelina Irén Kertay"]
  };
  
  return candidates[district] || [];
}

/**
 * Find a polling place for the given coordinates
 */
export function findNearestPollingPlace(lat: number, lon: number): PollingPlace {
  // Mock data - in a real app, this would be calculated based on actual polling locations
  const pollingPlaces = [
    {
      name: "Brainerd Recreation Center",
      address: "1010 N Moore Road, Chattanooga, TN 37411",
      precinct: "Precinct 12"
    },
    {
      name: "Hixson Community Center",
      address: "5401 School Drive, Chattanooga, TN 37343",
      precinct: "Precinct 8"
    },
    {
      name: "East Chattanooga YFD Center",
      address: "715 N Hickory St, Chattanooga, TN 37404",
      precinct: "Precinct 3"
    }
  ];
  
  // For demo purposes, just pick a random polling place
  const randomIndex = Math.floor(Math.random() * pollingPlaces.length);
  return pollingPlaces[randomIndex];
}

/**
 * Get comprehensive district information
 */
export function getDistrictInfo(lat: number, lon: number): DistrictInfo {
  const district = getDistrictForCoordinates(lat, lon);
  
  if (district === "District not found") {
    return {
      district_number: district,
      precinct: "Not found",
      polling_place: "Not found",
      polling_address: "Not found",
      distance: "N/A",
      error: "Location outside city limits",
      candidates: []
    };
  }
  
  const pollingPlace = findNearestPollingPlace(lat, lon);
  const candidates = getDistrictCandidates(district);
  const councilMember = getCouncilMember(district);
  
  return {
    district_number: district,
    district_description: `Chattanooga City Council District ${district}`,
    precinct: pollingPlace.precinct,
    polling_place: pollingPlace.name,
    polling_address: pollingPlace.address,
    distance: "Based on your location",
    candidates: candidates,
    council_member: councilMember
  };
} 