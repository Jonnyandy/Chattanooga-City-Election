"use client";

import { useState, useEffect, useCallback } from "react";
import { FiSearch, FiInfo, FiMapPin, FiHome } from "react-icons/fi";
import dynamic from "next/dynamic";
import DistrictInfo from "./DistrictInfo";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";

// Import map component dynamically to avoid SSR issues with Leaflet
const DistrictMap = dynamic(() => import("./DistrictMap"), {
  ssr: false,
  loading: () => (
    <div className="h-[450px] w-full flex items-center justify-center bg-gray-100 rounded-md">
      <div className="flex flex-col items-center">
        <svg className="animate-spin -ml-1 mr-3 h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span className="mt-2 text-blue-600 font-medium">Loading map...</span>
      </div>
    </div>
  ),
});

type CoordinatesType = [number, number] | null;

type DistrictInfoType = {
  district_number: string;
  district_description?: string;
  precinct: string;
  polling_place: string;
  polling_address: string;
  candidates: string[];
  council_member?: string;
  council_contact?: string;
  council_email?: string;
  council_member_status?: string;
  council_member_note?: string;
} | null;

export default function DistrictFinder() {
  const [streetAddress, setStreetAddress] = useState("");
  const [zipCode, setZipCode] = useState("");
  const [coordinates, setCoordinates] = useState<CoordinatesType>(null);
  const [districtInfo, setDistrictInfo] = useState<DistrictInfoType>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [useBrowserLocation, setUseBrowserLocation] = useState(false);

  const handleBrowserLocation = useCallback(async () => {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by your browser");
      return;
    }

    // Check if we're on HTTPS (required for geolocation in most browsers)
    if (typeof window !== 'undefined' && window.location.protocol !== 'https:' && window.location.hostname !== 'localhost') {
      setError("Location access requires HTTPS. Please use the address form instead.");
      return;
    }

    setLoading(true);
    setError(null);
    
    // Geolocation options for better accuracy and user experience
    const options = {
      enableHighAccuracy: true,
      timeout: 10000, // 10 second timeout
      maximumAge: 300000 // Accept 5-minute-old cached position
    };
    
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        setCoordinates([latitude, longitude]);
        setUseBrowserLocation(true);
        setSearchPerformed(true);
        
        try {
          // Look up the district based on the coordinates
          const districtResponse = await fetch(`/api/district?lat=${latitude}&lng=${longitude}`);
          
          if (!districtResponse.ok) {
            const errorData = await districtResponse.json();
            if (errorData.errorType === 'OUT_OF_BOUNDS' || errorData.errorType === 'NOT_IN_DISTRICT') {
              throw new Error(errorData.details || errorData.error);
            }
            throw new Error("Failed to find district for this location");
          }
          
          const districtData = await districtResponse.json();
          
          // The API now returns complete district information including candidates
          // Ensure candidates is always an array
          setDistrictInfo({
            ...districtData,
            candidates: districtData.candidates || []
          });
        } catch (err: any) {
          console.error("District lookup error:", err);
          setError(err.message || "Unable to find district for your location. Please try entering your address manually.");
        } finally {
          setLoading(false);
        }
      },
      (error) => {
        console.log("Geolocation error:", error);
        setLoading(false);
        let errorMessage = "Unable to retrieve your location. Please enter your address manually.";
        
        // Provide more specific error messages based on the error code
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = "Location access was denied. Please enable location services and try again, or enter your address manually.";
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = "Location information is unavailable. Please enter your address manually.";
            break;
          case error.TIMEOUT:
            errorMessage = "Location request timed out. Please try again or enter your address manually.";
            break;
          default:
            errorMessage = "An error occurred while retrieving your location. Please enter your address manually.";
        }
        
        setError(errorMessage);
        console.error("Geolocation error:", error);
      },
      options
    );
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!streetAddress || !zipCode) {
      setError("Please enter both street address and ZIP code");
      return;
    }
    
    setLoading(true);
    setError(null);
    setSearchPerformed(true);
    
    try {
      // First, geocode the address to get coordinates
      const fullAddress = `${streetAddress}, ${zipCode}`;
      const geocodeResponse = await fetch(`/api/geocode?q=${encodeURIComponent(fullAddress)}`);
      
      if (!geocodeResponse.ok) {
        const errorData = await geocodeResponse.json();
        throw new Error(errorData.error || "Failed to geocode address");
      }
      
      const geocodeData = await geocodeResponse.json();
      const coordinates: CoordinatesType = [geocodeData.lat, geocodeData.lon];
      setCoordinates(coordinates);
      
      // Then, look up the district based on the coordinates
      const districtResponse = await fetch(`/api/district?lat=${geocodeData.lat}&lng=${geocodeData.lon}`);
      
      if (!districtResponse.ok) {
        const errorData = await districtResponse.json();
        if (errorData.errorType === 'OUT_OF_BOUNDS' || errorData.errorType === 'NOT_IN_DISTRICT') {
          throw new Error(errorData.details || errorData.error);
        }
        throw new Error("Failed to find district for this location");
      }
      
      const districtData = await districtResponse.json();
      
      // The API now returns complete district information including candidates
      // Ensure candidates is always an array
      setDistrictInfo({
        ...districtData,
        candidates: districtData.candidates || []
      });
      
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error finding your district. Please try again.");
      console.error("Search error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch(e as any);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-xl font-semibold">Find Your District</CardTitle>
          <CardDescription>
            Enter your address to find your City Council district and polling location
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-2">
                <label htmlFor="street-address" className="block text-sm font-medium text-gray-700 mb-1">
                  Street Address
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <FiHome className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="text"
                    id="street-address"
                    placeholder="123 Main St"
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={streetAddress}
                    onChange={(e) => setStreetAddress(e.target.value)}
                    onKeyDown={handleKeyDown}
                  />
                </div>
              </div>
              
              <div>
                <label htmlFor="zip-code" className="block text-sm font-medium text-gray-700 mb-1">
                  ZIP Code
                </label>
                <input
                  type="text"
                  id="zip-code"
                  placeholder="37402"
                  className="px-4 py-2 border border-gray-300 rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={zipCode}
                  onChange={(e) => setZipCode(e.target.value)}
                  onKeyDown={handleKeyDown}
                  maxLength={5}
                />
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
              <Button 
                type="submit" 
                className="bg-blue-600 hover:bg-blue-700 text-white"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Searching...
                  </>
                ) : (
                  <>
                    <FiSearch className="mr-2" />
                    Find My District
                  </>
                )}
              </Button>
              
              <Button
                type="button"
                variant="outline"
                onClick={handleBrowserLocation}
                disabled={loading}
                className="flex items-center justify-center"
              >
                <FiMapPin className="mr-2" />
                Use My Current Location
              </Button>
            </div>
          </form>
          
          {error && (
            <Alert variant="destructive" className="mt-4">
              <AlertDescription>
                <div className="space-y-2">
                  <p>{error}</p>
                  {error.includes('city limits') && (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3 mt-2">
                      <p className="text-sm text-yellow-800">
                        <strong>Need help?</strong> If you believe this address should be within Chattanooga city limits:
                      </p>
                      <ul className="text-sm text-yellow-700 mt-1 list-disc list-inside space-y-1">
                        <li>Double-check your address spelling and ZIP code</li>
                        <li>Try adding "Chattanooga, TN" to your address</li>
                        <li>Some areas may be in unincorporated Hamilton County rather than the city</li>
                        <li>Contact Hamilton County Election Commission at (423) 209-6300 for assistance</li>
                      </ul>
                    </div>
                  )}
                </div>
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
      
      {searchPerformed && !loading && !error && (
        <div className="space-y-6">
          <Card>
            <CardContent className="pt-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold mb-4">Your District Information</h3>
                  
                  {districtInfo ? (
                    <div className="space-y-4">
                      <div>
                        <Badge variant="outline" className="mb-2 text-lg font-bold bg-blue-50 text-blue-800 border-blue-200 px-3 py-1">
                          District {districtInfo.district_number}
                        </Badge>
                        <p className="text-gray-600">{districtInfo.precinct}</p>
                      </div>
                      
                      {districtInfo.council_member && (
                        <div>
                          <h4 className="font-medium text-gray-700">Current Council Member:</h4>
                          <p className="font-semibold">{districtInfo.council_member}</p>
                          {districtInfo.council_contact && (
                            <p className="text-sm text-gray-600">📞 {districtInfo.council_contact}</p>
                          )}
                          {districtInfo.council_email && (
                            <p className="text-sm text-gray-600">✉️ {districtInfo.council_email}</p>
                          )}
                          {districtInfo.council_member_note && (
                            <p className="text-sm text-orange-600 mt-1">ℹ️ {districtInfo.council_member_note}</p>
                          )}
                        </div>
                      )}
                      
                      <Separator />
                      
                      <div>
                        <h4 className="font-medium text-gray-700">Polling Information:</h4>
                        <p className="text-sm text-gray-600 mb-2">{districtInfo.precinct}</p>
                        <p className="font-medium">{districtInfo.polling_place}</p>
                        <p className="text-sm text-gray-600">{districtInfo.polling_address}</p>
                      </div>
                      
                      <Separator />
                      
                      <div>
                        <h4 className="font-medium text-gray-700 mb-2">
                          {districtInfo.candidates && districtInfo.candidates.length > 0 ? 'Election Candidates:' : 'No Candidates Running'}
                        </h4>
                        {districtInfo.candidates && districtInfo.candidates.length > 0 ? (
                          <ul className="space-y-1">
                            {districtInfo.candidates.map((candidate, index) => (
                              <li key={index} className="flex items-center">
                                <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                                {candidate}
                              </li>
                            ))}
                          </ul>
                        ) : (
                          <p className="text-sm text-gray-500">No candidates are running for this district in the current election.</p>
                        )}
                      </div>
                      
                      <div className="pt-2">
                        <Button asChild variant="outline">
                          <a href={`/candidates?district=${districtInfo.district_number}`}>
                            View All Candidates in District {districtInfo.district_number}
                          </a>
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <p className="text-gray-500">District information not available</p>
                    </div>
                  )}
                </div>
                
                <div className="h-[350px] md:h-auto">
                  {coordinates && (
                    <DistrictMap 
                      selectedCoordinates={coordinates} 
                      selectedDistrict={districtInfo?.district_number || null}
                      onSelectDistrict={(district) => console.log("Selected district:", district)}
                    />
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
          
          {districtInfo && (
            <DistrictInfo districtInfo={districtInfo} />
          )}
        </div>
      )}
    </div>
  );
} 