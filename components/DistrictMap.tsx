"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON, Marker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix icon issues in leaflet with Next.js
// For production, import these resources properly
const icon = L.icon({
  iconUrl: "/images/marker-icon.png",
  shadowUrl: "/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

// Map recenter component
function RecenterMap({ position }: { position: [number, number] | null }) {
  const map = useMap();
  
  useEffect(() => {
    if (position) {
      map.setView(position, 14);
    }
  }, [map, position]);
  
  return null;
}

type MapProps = {
  selectedCoordinates: [number, number] | null;
  selectedDistrict: string | null;
  onSelectDistrict: (district: string) => void;
};

export default function DistrictMap({
  selectedCoordinates,
  selectedDistrict,
  onSelectDistrict,
}: MapProps) {
  const [geoJsonData, setGeoJsonData] = useState<any>(null);

  useEffect(() => {
    fetch("/api/geojson")
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          setGeoJsonData(data.data);
        }
      })
      .catch((error) => {
        console.error("Error loading GeoJSON data:", error);
      });
  }, []);

  // Style function for district polygons
  const style = (feature: any) => {
    // Check both property formats for district identification
    const districtId = feature.properties?.district || (feature.properties?.name ? feature.properties.name.replace('District ', '') : '');
    const isSelected = selectedDistrict && districtId === selectedDistrict;
    
    return {
      fillColor: isSelected ? "#3388ff" : "#9ecae1",
      weight: isSelected ? 3 : 1,
      opacity: 1,
      color: isSelected ? "#0056b3" : "#666",
      fillOpacity: isSelected ? 0.7 : 0.5,
    };
  };

  // Event handler for each district
  const onEachFeature = (feature: any, layer: L.Layer) => {
    // Check both property names - 'district' (old format) and 'name' (new format)
    const districtId = feature.properties?.district || feature.properties?.name?.replace('District ', '') || '';
    
    if (districtId) {
      layer.on({
        click: () => {
          onSelectDistrict(districtId);
        },
      });
      
      layer.bindTooltip(`District ${districtId}`, {
        permanent: false,
        direction: "center",
        className: "district-tooltip",
      });
    }
  };

  return (
    <MapContainer
      center={[35.0458, -85.3094]} // Chattanooga center
      zoom={11}
      style={{ height: "100%", width: "100%" }}
      zoomControl={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      {geoJsonData && (
        <GeoJSON
          data={geoJsonData}
          style={style}
          onEachFeature={onEachFeature}
        />
      )}
      
      {selectedCoordinates && (
        <Marker position={selectedCoordinates} icon={icon}>
          <Popup>Your location</Popup>
        </Marker>
      )}
      
      {selectedCoordinates && <RecenterMap position={selectedCoordinates} />}
    </MapContainer>
  );
} 