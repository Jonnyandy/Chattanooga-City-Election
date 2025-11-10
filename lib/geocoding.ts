// This is the TypeScript equivalent of your Python geocoding utility

// Helper types
type Coordinates = [number, number]; // [latitude, longitude]

// Chattanooga ZIP code validation - matches the Python implementation
const CHATTANOOGA_ZIP_CODES = new Set([
  '37401', '37402', '37403', '37404', '37405', '37406', 
  '37407', '37408', '37409', '37410', '37411', '37412', 
  '37415', '37416', '37419', '37421', '37450', '37351'
]);

/**
 * Validates if the input address is in Chattanooga based on ZIP code
 */
export function validateAddress(address: string): boolean {
  if (!address) return false;
  
  // Extract ZIP code from address with regex
  const zipMatch = address.match(/\b\d{5}\b/);
  if (!zipMatch) return false;
  
  const zipCode = zipMatch[0];
  return CHATTANOOGA_ZIP_CODES.has(zipCode);
}

/**
 * Mock geocoding function to mimic the Python implementation
 * In a real app, you would use a service like Google Maps, Mapbox, etc.
 */
export async function geocodeAddress(address: string): Promise<Coordinates | null> {
  try {
    // Clean address
    const cleanAddress = address.trim();
    
    // Add location context if missing
    let processedAddress = cleanAddress;
    if (!cleanAddress.toLowerCase().includes('chattanooga')) {
      processedAddress = `${cleanAddress}, Chattanooga, TN`;
    } else if (!cleanAddress.toLowerCase().includes('tn') && 
              !cleanAddress.toLowerCase().includes('tennessee')) {
      processedAddress = `${cleanAddress}, TN`;
    }
    
    // In a real app, you would call a geocoding service here
    // For demo purposes, we'll generate a random location in Chattanooga
    
    // Chattanooga bounds (approximately)
    const CHATTANOOGA_BOUNDS = {
      north: 35.2, // North latitude
      south: 34.9, // South latitude
      east: -85.1, // East longitude
      west: -85.4  // West longitude
    };
    
    // Check if the address has a valid Chattanooga ZIP
    if (!validateAddress(cleanAddress)) {
      return null;
    }
    
    // Generate a random location within Chattanooga bounds
    // In a real app, this would be replaced with actual geocoding
    const randomLat = Math.random() * (CHATTANOOGA_BOUNDS.north - CHATTANOOGA_BOUNDS.south) + CHATTANOOGA_BOUNDS.south;
    const randomLng = Math.random() * (CHATTANOOGA_BOUNDS.east - CHATTANOOGA_BOUNDS.west) + CHATTANOOGA_BOUNDS.west;
    
    return [randomLat, randomLng];
  } catch (error) {
    console.error("Geocoding error:", error);
    return null;
  }
} 