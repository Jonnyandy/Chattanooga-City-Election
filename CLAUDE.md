# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run typecheck` - Run TypeScript type checking

## Project Architecture

This is a Next.js 14 application for the Chattanooga City Council Election, built with TypeScript and Tailwind CSS. The app helps users find their city council district, learn about candidates, and get voting information.

### Key Technologies
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** with shadcn/ui components
- **Leaflet** for interactive maps
- **OpenStreetMap Nominatim** for geocoding
- **GeoJSON** for district boundary data

### Core Structure

**App Router Structure:**
- `app/` - Main application using Next.js App Router
  - `page.tsx` - Home page with district finder
  - `candidates/page.tsx` - Candidate information
  - `how-to-vote/page.tsx` - Voting instructions
  - `media/page.tsx` - Media resources
  - `reliable-map/page.tsx` - Alternative map implementation
  - `api/` - API routes for district lookup and geocoding
  - `actions/` - Server actions
  - `components/` - App-specific components
  - `services/` - Service layer

**Shared Components:**
- `components/` - Reusable UI components
  - `ui/` - shadcn/ui components
  - Map components (DistrictMap, LeafletMap, etc.)
  - Candidate components
  - Layout components (Sidebar, etc.)

**Data Layer:**
- `data/` - Static data files
  - `Current City Council Districts_20250331.geojson` - District boundaries
  - `candidates.json` - Candidate information
  - `districts.json` - District data
  - `council_members.json` - Current council members

**Libraries:**
- `lib/` - Shared utilities
  - `district-data.ts` - District data fetching and processing
  - `utils.ts` - General utilities (includes shadcn/ui cn function)

### District Data System

The app uses a hierarchical data loading system:
1. **Primary**: GeoJSON file with district boundaries
2. **Fallback**: Generated districts if GeoJSON fails to load
3. **Service Layer**: `districtService.ts` handles all district-related operations

The district system supports:
- Point-in-polygon detection for address-to-district mapping
- Interactive map rendering with Leaflet
- Demographic data display
- Council member information

### Map Implementation

Two map implementations are available:
1. **Primary Map** (`DistrictMap.tsx`) - Full-featured interactive map
2. **Reliable Map** (`ReliableMap.tsx`) - Simplified fallback option

Both use react-leaflet and support:
- District boundary visualization
- User location detection
- Address geocoding via OpenStreetMap Nominatim API
- Responsive design

### Styling System

- **Tailwind CSS** with custom configuration
- **shadcn/ui** component library
- **CSS Variables** for theming
- **Responsive design** with mobile-first approach

### Configuration Notes

- **Next.js Config**: Configured for large GeoJSON files with increased page data limits
- **TypeScript**: Strict mode enabled with path aliases (`@/*`)
- **Tailwind**: Extended with shadcn/ui theme system
- **Geocoding**: Uses OpenStreetMap Nominatim API (no API key required)

### Development Patterns

- Use TypeScript interfaces for all data structures
- Follow Next.js App Router patterns
- Implement proper error handling for map/geocoding failures
- Use shadcn/ui components for consistent UI
- Maintain responsive design across all components