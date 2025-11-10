"use client";

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { FiMail, FiPhone, FiGlobe, FiPlayCircle, FiInfo, FiSearch, FiChevronDown, FiChevronUp } from "react-icons/fi";
import { FaFacebook, FaInstagram, FaLinkedin, FaTwitter, FaVoteYea } from "react-icons/fa";
import Image from "next/image";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import CandidateImage from "./CandidateImage";

type Candidate = {
  id: string;
  name: string;
  district: string;
  party?: string;
  slogan?: string;
  bio?: string;
  website?: string;
  facebook?: string;
  twitter?: string;
  instagram?: string;
  email?: string;
  phone?: string;
  image?: string;
  videoId?: string;
  incumbent: boolean;
};

type CandidatesListProps = {
  district: string;
};

// Enhanced candidate data with more complete information
const candidatesData: Candidate[] = [
  // Mayoral candidates
  {
    id: 'tim-kelly',
    name: 'Tim Kelly',
    district: 'Mayor',
    website: 'https://kellyforchatanooga.com',
    facebook: 'https://facebook.com/timkellyformayor',
    twitter: 'https://twitter.com/timkellychatt',
    instagram: 'https://instagram.com/timkellyformayor',
    email: 'info@kellyforchatanooga.com',
    image: '/images/candidate_photos/Tim_Kelly.jpg',
    incumbent: true,
    slogan: 'One Chattanooga',
    bio: 'Tim Kelly is the current Mayor of Chattanooga, elected in 2021. He is a business owner and community leader with deep Chattanooga roots.'
  },
  {
    id: 'chris-long',
    name: 'Chris Long',
    district: 'Mayor',
    website: 'https://chrislong4mayor.com',
    facebook: 'https://facebook.com/ChrisLongforMayor',
    email: 'info@chrislong4mayor.com',
    image: '/images/candidate_photos/Chris_Long.jpg',
    incumbent: false,
    slogan: 'Leadership for a Better Chattanooga',
    bio: 'Chris Long is a business leader and community advocate running to bring new leadership to City Hall.'
  },
  
  // District 1
  {
    id: 'chip-henderson',
    name: 'Chip Henderson',
    district: '1',
    website: 'https://chiphenderson.com',
    facebook: 'https://facebook.com/ChipHendersonDistrict1',
    email: 'chip@chiphenderson.com',
    image: '/images/candidate_photos/Chip_Henderson.jpg',
    incumbent: true,
    slogan: 'Experienced Leadership',
    bio: 'Chip Henderson has represented District 1 since 2013. He is focused on infrastructure, public safety, and economic development.'
  },
  {
    id: 'james-burnette',
    name: 'James "Skip" Burnette',
    district: '1',
    facebook: 'https://facebook.com/SkipForDistrict1',
    email: 'skip4district1@gmail.com',
    image: '/images/candidate_photos/James_Skip_Burnette.jpg',
    incumbent: false,
    slogan: 'A Fresh Voice for District 1',
    bio: 'Skip Burnette is a small business owner and lifelong resident of District 1 who wants to bring fresh ideas to the City Council.'
  },
  
  // District 2
  {
    id: 'jenny-hill',
    name: 'Jenny Hill',
    district: '2',
    website: 'https://votejennyhill.org',
    facebook: 'https://facebook.com/VoteJennyHill',
    twitter: 'https://twitter.com/VoteJennyHill',
    email: 'info@votejennyhill.org',
    image: '/images/candidate_photos/Jenny_Hill.jpg',
    incumbent: true,
    slogan: 'Building Community Together',
    bio: 'Jenny Hill is a former Hamilton County School Board member now serving District 2 on the City Council. Her focus is on education, housing, and community development.'
  },
  
  // District 3
  {
    id: 'jeff-davis',
    name: 'Jeff Davis',
    district: '3',
    facebook: 'https://facebook.com/JeffDavisDistrict3',
    email: 'jeff4district3@gmail.com',
    image: '/images/candidate_photos/Jeff_Davis.jpg',
    incumbent: false,
    slogan: 'Accountability & Results',
    bio: 'Jeff Davis is a local business owner and community advocate focused on responsible growth and neighborhood preservation.'
  },
  {
    id: 'tom-marshall',
    name: 'Tom Marshall',
    district: '3',
    website: 'https://marshallfordistrict3.com',
    facebook: 'https://facebook.com/MarshallForDistrict3',
    email: 'info@marshallfordistrict3.com',
    image: '/images/candidate_photos/Tom_Marshall.jpg',
    incumbent: false,
    slogan: 'New Ideas for District 3',
    bio: 'Tom Marshall is an architect and long-time resident of District 3 who wants to improve infrastructure and create sustainable development.'
  },
  
  // District 4
  {
    id: 'cody-harvey',
    name: 'Cody Harvey',
    district: '4',
    facebook: 'https://facebook.com/CodyHarveyDistrict4',
    email: 'cody4district4@gmail.com',
    image: '/images/candidate_photos/Cody_Harvey.jpg',
    incumbent: false,
    slogan: 'Progress for Our Community',
    bio: 'Cody Harvey is a community organizer and small business advocate who wants to bring more resources to District 4.'
  },
  
  // District 5
  {
    id: 'isiah-hester',
    name: 'Isiah "Ike" Hester',
    district: '5',
    email: 'isiahhester4district5@gmail.com',
    image: '/images/candidate_photos/Isiah_Ike_Hester.jpg',
    incumbent: true,
    slogan: 'Committed to Community',
    bio: 'Isiah "Ike" Hester is serving District 5 with a focus on neighborhood safety, economic development, and community empowerment.'
  },
  
  // District 6
  {
    id: 'carol-berz',
    name: 'Jenni Berz',
    district: '6',
    website: 'https://jenniberz.com',
    facebook: 'https://facebook.com/JenniBerzDistrict6',
    email: 'info@jenniberz.com',
    image: '/images/candidate_photos/Jenni_Berz.jpg',
    incumbent: false,
    slogan: 'Working Together for District 6',
    bio: 'Jenni Berz is a nonprofit leader and community advocate focused on inclusive growth and neighborhood improvement for District 6.'
  },
  
  // District 7
  {
    id: 'raquetta-dotley',
    name: 'Raquetta Dotley',
    district: '7',
    website: 'https://raquettadotley.com',
    facebook: 'https://facebook.com/RaquettaDotleyForDistrict7',
    email: 'info@raquettadotley.com',
    image: '/images/candidate_photos/Raquetta_Dotley.jpg',
    incumbent: true,
    slogan: 'Standing Up for District 7',
    bio: 'Raquetta Dotley is a community leader focused on affordable housing, economic opportunity, and public safety for District 7 residents.'
  },
  
  // District 8
  {
    id: 'marvene-noel',
    name: 'Marvene Noel',
    district: '8',
    facebook: 'https://facebook.com/MarveneNoelDistrict8',
    email: 'marvenenoel@gmail.com',
    image: '/images/candidate_photos/Marvene_Noel.jpg',
    incumbent: true,
    slogan: 'Leadership That Listens',
    bio: 'Marvene Noel represents District 8 with a focus on community empowerment, economic development, and quality of life improvements.'
  },
  
  // District 9
  {
    id: 'demetrus-coonrod',
    name: 'Demetrus Coonrod',
    district: '9',
    website: 'https://demetruscoonrod.com',
    facebook: 'https://facebook.com/DemetrusCoonrodDistrict9',
    email: 'info@demetruscoonrod.com',
    image: '/images/candidate_photos/Doll_Sandridge.jpg', // Using available photo as placeholder
    incumbent: true,
    slogan: 'Advocating for All',
    bio: 'Demetrus Coonrod serves District 9 focusing on equitable development, affordable housing, and community safety.'
  },
  
  // Additional candidates
  {
    id: 'ron-elliott',
    name: 'Ron Elliott',
    district: '9',
    email: 'info@ronelliott.com',
    image: '/images/candidate_photos/Ron_Elliott.jpg',
    incumbent: false,
    slogan: 'A New Vision',
    bio: 'Ron Elliott is running to bring new ideas and representation to District 9.'
  },
  {
    id: 'samantha-reid-hawkins',
    name: 'Samantha Reid-Hawkins',
    district: '5',
    email: 'samanthareid4district5@gmail.com',
    image: '/images/candidate_photos/Samantha_Reid-Hawkins.jpg',
    incumbent: false,
    slogan: 'Community First',
    bio: 'Samantha Reid-Hawkins is committed to addressing the unique needs of District 5 residents.'
  },
  {
    id: 'mark-holland',
    name: 'Mark Holland',
    district: '6',
    website: 'https://markholland.vote',
    image: '/images/candidate_photos/Mark_Holland.jpg',
    incumbent: false,
    slogan: 'Building a Better District 6',
    bio: 'Mark Holland is focused on infrastructure improvements and economic development for District 6.'
  },
  {
    id: 'kelvin-scott',
    name: 'Kelvin Scott',
    district: '8',
    email: 'kelvinscott4district8@gmail.com',
    image: '/images/candidate_photos/Kelvin_Scott.jpg',
    incumbent: false,
    slogan: 'A Fresh Perspective',
    bio: 'Kelvin Scott aims to bring innovative solutions to the challenges facing District 8.'
  },
  {
    id: 'evelina-kertay',
    name: 'Evelina Irén Kertay',
    district: '9',
    email: 'evelinakertay4district9@gmail.com',
    image: '/images/candidate_photos/Evelina_Irén_Kertay.jpg',
    incumbent: false,
    slogan: 'Inclusive Leadership',
    bio: 'Evelina Irén Kertay is committed to ensuring all voices in District 9 are heard and represented.'
  },
  {
    id: 'dennis-clark',
    name: 'Dennis Clark',
    district: '5',
    image: '/images/candidate_photos/Dennis_Clark.jpg',
    incumbent: false,
    slogan: 'Working for Change',
    bio: 'Dennis Clark is focused on bringing positive change to District 5 through community engagement and responsive leadership.'
  },
  {
    id: 'christian-siler',
    name: 'Christian Siler',
    district: '6',
    image: '/images/candidate_photos/Christian_Siler.jpg',
    incumbent: false,
    slogan: 'New Energy for District 6',
    bio: 'Christian Siler brings a fresh perspective and energy to addressing the challenges facing District 6.'
  },
  {
    id: 'cory-hall',
    name: 'Cory Hall',
    district: '5',
    image: '/images/candidate_photos/Cory_Hall.jpg',
    incumbent: false,
    slogan: 'Rebuilding Together',
    bio: 'Cory Hall is dedicated to rebuilding and strengthening the community in District 5.'
  },
  {
    id: 'anna-golladay',
    name: 'Anna Golladay',
    district: '8',
    image: '/images/candidate_photos/Anna_Golladay.jpg',
    incumbent: false,
    slogan: 'Progress Through Unity',
    bio: 'Anna Golladay is committed to bringing the community together to address the challenges facing District 8.'
  },
  {
    id: 'jennifer-gregory',
    name: 'Jennifer Gregory',
    district: '6',
    image: '/images/candidate_photos/Jennifer_Gregory.jpg',
    incumbent: false,
    slogan: 'Community Voice',
    bio: 'Jennifer Gregory is dedicated to being a strong voice for the residents of District 6.'
  },
  {
    id: 'letechia-ellis',
    name: 'Letechia Ellis',
    district: '9',
    image: '/images/candidate_photos/Letechia_Ellis.jpg',
    incumbent: false,
    slogan: 'Committed to Service',
    bio: 'Letechia Ellis is focused on community service and advocacy for the residents of District 9.'
  },
  {
    id: 'robert-wilson',
    name: 'Robert C. Wilson',
    district: '6',
    image: '/images/candidate_photos/Robert_C_Wilson.jpg',
    incumbent: false,
    slogan: 'Experience Matters',
    bio: 'Robert C. Wilson brings years of experience and a deep commitment to serving the residents of District 6.'
  },
  {
    id: 'doll-sandridge',
    name: 'Doll Sandridge',
    district: '8',
    image: '/images/candidate_photos/Doll_Sandridge.jpg',
    incumbent: false,
    slogan: 'Community Leadership',
    bio: 'Doll Sandridge is committed to bringing strong community leadership to District 8.'
  }
];

export default function CandidatesList({ district }: CandidatesListProps) {
  // States for UI features
  const [selectedDistrict, setSelectedDistrict] = useState(district);
  const [searchTerm, setSearchTerm] = useState("");
  const [showIncumbentsOnly, setShowIncumbentsOnly] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [isVideoDialogOpen, setIsVideoDialogOpen] = useState(false);
  
  // Verify candidate data on component mount
  useEffect(() => {
    // Check and log any potential issues with image paths
    candidatesData.forEach(candidate => {
      if (candidate.image) {
        // Check for common problems in file paths
        if (candidate.image.includes(' ')) {
          console.warn(`Candidate ${candidate.name} has space in image path: ${candidate.image}`);
        }
        
        if (candidate.image.includes('(') || candidate.image.includes(')')) {
          console.warn(`Candidate ${candidate.name} has parentheses in image path: ${candidate.image}`);
        }
        
        // Verify the path starts with /
        if (!candidate.image.startsWith('/')) {
          console.warn(`Candidate ${candidate.name} image path should start with /: ${candidate.image}`);
        }
      } else {
        console.warn(`Candidate ${candidate.name} has no image path defined`);
      }
    });
  }, []);
  
  // Filter candidates based on the selected district and search terms
  const filterCandidates = useCallback(() => {
    let filtered = selectedDistrict === 'All' 
      ? candidatesData.filter(c => c.district !== 'Mayor') 
      : candidatesData.filter(c => c.district === selectedDistrict);
    
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(c => 
        c.name.toLowerCase().includes(term) || 
        c.bio?.toLowerCase().includes(term) ||
        c.slogan?.toLowerCase().includes(term)
      );
    }
    
    if (showIncumbentsOnly) {
      filtered = filtered.filter(c => c.incumbent);
    }
    
    return filtered;
  }, [selectedDistrict, searchTerm, showIncumbentsOnly]);
  
  const filteredCandidates = filterCandidates();
  
  // Handle district change
  const handleDistrictChange = (newDistrict: string) => {
    setSelectedDistrict(newDistrict);
  };
  
  return (
    <div className="space-y-6">
      {/* Search and filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0 md:space-x-4">
            <div className="relative flex-1 md:max-w-md">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <FiSearch className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search candidates..."
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="incumbents-only"
                className="rounded text-blue-600 focus:ring-blue-500 h-4 w-4"
                checked={showIncumbentsOnly}
                onChange={(e) => setShowIncumbentsOnly(e.target.checked)}
              />
              <label htmlFor="incumbents-only" className="text-sm font-medium text-gray-700">
                Incumbents Only
              </label>
            </div>
            
            {selectedDistrict !== 'Mayor' && (
              <div className="relative">
                <select
                  className="appearance-none bg-white border border-gray-300 rounded-md pl-4 pr-10 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={selectedDistrict}
                  onChange={(e) => handleDistrictChange(e.target.value)}
                >
                  <option value="All">All Districts</option>
                  <option value="1">District 1</option>
                  <option value="2">District 2</option>
                  <option value="3">District 3</option>
                  <option value="4">District 4</option>
                  <option value="5">District 5</option>
                  <option value="6">District 6</option>
                  <option value="7">District 7</option>
                  <option value="8">District 8</option>
                  <option value="9">District 9</option>
                </select>
                <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                  <FiChevronDown className="h-4 w-4 text-gray-500" />
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
      
      {/* Results count */}
      <div className="text-sm text-gray-600">
        {filteredCandidates.length === 0 ? (
          <p>No candidates found. Try adjusting your search or filters.</p>
        ) : (
          <p>Showing {filteredCandidates.length} candidate{filteredCandidates.length !== 1 ? 's' : ''}</p>
        )}
      </div>
      
      {/* Candidates grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCandidates.map(candidate => (
          <CandidateCard 
            key={candidate.id} 
            candidate={candidate} 
            onSelect={() => setSelectedCandidate(candidate)}
            onVideoClick={() => {
              setSelectedCandidate(candidate);
              setIsVideoDialogOpen(true);
            }}
          />
        ))}
      </div>
      
      {/* Candidate detail dialog */}
      <Dialog open={!!selectedCandidate && !isVideoDialogOpen} onOpenChange={(open) => !open && setSelectedCandidate(null)}>
        {selectedCandidate && (
          <DialogContent className="sm:max-w-3xl">
            <DialogHeader>
              <DialogTitle className="text-2xl font-bold text-blue-800">{selectedCandidate.name}</DialogTitle>
              <DialogDescription>
                {selectedCandidate.district === 'Mayor' ? 'Mayoral Candidate' : `District ${selectedCandidate.district} Candidate`}
                {selectedCandidate.incumbent && (
                  <Badge variant="secondary" className="ml-2 bg-blue-100 text-blue-800">Incumbent</Badge>
                )}
              </DialogDescription>
            </DialogHeader>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="md:col-span-1">
                <div className="relative aspect-square w-full overflow-hidden rounded-lg">
                  {selectedCandidate.image ? (
                    <CandidateImage
                      src={selectedCandidate.image}
                      alt={selectedCandidate.name}
                      className="rounded-lg"
                    />
                  ) : (
                    <div className="h-full w-full flex items-center justify-center bg-gray-100 text-gray-400">
                      No photo available
                    </div>
                  )}
                </div>
                
                <div className="mt-4 space-y-3">
                  {selectedCandidate.email && (
                    <div className="flex items-center">
                      <FiMail className="text-blue-600 mr-2" />
                      <a href={`mailto:${selectedCandidate.email}`} className="text-blue-600 hover:underline">
                        {selectedCandidate.email}
                      </a>
                    </div>
                  )}
                  
                  {selectedCandidate.phone && (
                    <div className="flex items-center">
                      <FiPhone className="text-blue-600 mr-2" />
                      <a href={`tel:${selectedCandidate.phone}`} className="text-blue-600 hover:underline">
                        {selectedCandidate.phone}
                      </a>
                    </div>
                  )}
                  
                  {selectedCandidate.website && (
                    <div className="flex items-center">
                      <FiGlobe className="text-blue-600 mr-2" />
                      <a href={selectedCandidate.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                        Campaign Website
                      </a>
                    </div>
                  )}
                </div>
                
                <div className="mt-4 flex space-x-3">
                  {selectedCandidate.facebook && (
                    <a href={selectedCandidate.facebook} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                      <FaFacebook size={24} />
                    </a>
                  )}
                  
                  {selectedCandidate.twitter && (
                    <a href={selectedCandidate.twitter} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-600">
                      <FaTwitter size={24} />
                    </a>
                  )}
                  
                  {selectedCandidate.instagram && (
                    <a href={selectedCandidate.instagram} target="_blank" rel="noopener noreferrer" className="text-pink-600 hover:text-pink-800">
                      <FaInstagram size={24} />
                    </a>
                  )}
                </div>
              </div>
              
              <div className="md:col-span-2 space-y-4">
                {selectedCandidate.slogan && (
                  <div>
                    <h3 className="text-lg font-medium text-gray-500">Campaign Slogan</h3>
                    <p className="text-xl font-semibold text-blue-700">"{selectedCandidate.slogan}"</p>
                  </div>
                )}
                
                {selectedCandidate.bio && (
                  <div>
                    <h3 className="text-lg font-medium text-gray-500">About</h3>
                    <p className="text-gray-800">{selectedCandidate.bio}</p>
                  </div>
                )}
                
                {selectedCandidate.videoId && (
                  <div className="mt-4">
                    <Button 
                      onClick={() => setIsVideoDialogOpen(true)}
                      className="flex items-center space-x-2"
                    >
                      <FiPlayCircle />
                      <span>Watch Campaign Video</span>
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </DialogContent>
        )}
      </Dialog>
      
      {/* Video dialog */}
      <Dialog open={isVideoDialogOpen} onOpenChange={(open) => !open && setIsVideoDialogOpen(false)}>
        {selectedCandidate && selectedCandidate.videoId && (
          <DialogContent className="sm:max-w-4xl">
            <DialogHeader>
              <DialogTitle>{selectedCandidate.name} - Campaign Video</DialogTitle>
            </DialogHeader>
            <div className="aspect-video w-full">
              <iframe
                width="100%"
                height="100%"
                src={`https://www.youtube.com/embed/${selectedCandidate.videoId}`}
                title={`${selectedCandidate.name} campaign video`}
                style={{border: 0}}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            </div>
          </DialogContent>
        )}
      </Dialog>
    </div>
  );
}

function CandidateCard({ 
  candidate, 
  onSelect,
  onVideoClick 
}: { 
  candidate: Candidate; 
  onSelect: () => void;
  onVideoClick: () => void;
}) {
  
  return (
    <Card className="h-full flex flex-col overflow-hidden hover:shadow-md transition-shadow">
      {/* Candidate photo */}
      <div className="relative aspect-square w-full bg-gray-100">
        {candidate.image ? (
          <CandidateImage
            src={candidate.image}
            alt={candidate.name}
            className="rounded-t-lg"
          />
        ) : (
          <div className="h-full w-full flex items-center justify-center text-gray-400">
            <span className="text-center">No photo available</span>
          </div>
        )}
        
        {/* Incumbent badge */}
        {candidate.incumbent && (
          <Badge className="absolute top-2 right-2 bg-blue-600">
            <FaVoteYea className="mr-1" />
            Incumbent
          </Badge>
        )}
        
        {/* Video button */}
        {candidate.videoId && (
          <Button 
            variant="outline" 
            size="icon"
            className="absolute bottom-2 right-2 bg-white/80 hover:bg-white"
            onClick={(e) => {
              e.stopPropagation();
              onVideoClick();
            }}
          >
            <FiPlayCircle className="h-5 w-5 text-blue-600" />
          </Button>
        )}
      </div>
      
      {/* Candidate info */}
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-semibold text-blue-800">{candidate.name}</CardTitle>
        <CardDescription>
          {candidate.district === 'Mayor' ? 'Mayoral Candidate' : `District ${candidate.district} Candidate`}
        </CardDescription>
      </CardHeader>
      
      <CardContent className="flex-grow">
        {candidate.slogan && (
          <p className="text-sm italic text-gray-600 mb-3">"{candidate.slogan}"</p>
        )}
        
        {candidate.bio && (
          <p className="text-sm text-gray-700 line-clamp-3">
            {candidate.bio}
          </p>
        )}
      </CardContent>
      
      <CardFooter className="pt-0 flex justify-between items-center">
        <div className="flex space-x-2">
          {candidate.website && (
            <HoverCard>
              <HoverCardTrigger asChild>
                <a 
                  href={candidate.website} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800"
                  onClick={(e) => e.stopPropagation()}
                >
                  <FiGlobe size={18} />
                </a>
              </HoverCardTrigger>
              <HoverCardContent className="w-80">
                <div className="flex justify-between space-x-4">
                  <div className="space-y-1">
                    <h4 className="text-sm font-semibold">Campaign Website</h4>
                    <p className="text-sm">
                      Visit {candidate.name}'s official campaign website
                    </p>
                  </div>
                </div>
              </HoverCardContent>
            </HoverCard>
          )}
          
          {candidate.email && (
            <HoverCard>
              <HoverCardTrigger asChild>
                <a 
                  href={`mailto:${candidate.email}`} 
                  className="text-blue-600 hover:text-blue-800"
                  onClick={(e) => e.stopPropagation()}
                >
                  <FiMail size={18} />
                </a>
              </HoverCardTrigger>
              <HoverCardContent className="w-80">
                <div className="flex justify-between space-x-4">
                  <div className="space-y-1">
                    <h4 className="text-sm font-semibold">Contact via Email</h4>
                    <p className="text-sm">{candidate.email}</p>
                  </div>
                </div>
              </HoverCardContent>
            </HoverCard>
          )}
          
          {candidate.facebook && (
            <a 
              href={candidate.facebook} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="text-blue-600 hover:text-blue-800"
              onClick={(e) => e.stopPropagation()}
            >
              <FaFacebook size={18} />
            </a>
          )}
          
          {candidate.twitter && (
            <a 
              href={candidate.twitter} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="text-blue-400 hover:text-blue-600"
              onClick={(e) => e.stopPropagation()}
            >
              <FaTwitter size={18} />
            </a>
          )}
        </div>
        
        <Button variant="ghost" size="sm" onClick={onSelect}>
          View Profile
        </Button>
      </CardFooter>
    </Card>
  );
} 