"use client";

import { useState, useEffect, useRef } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { FiPlay } from "react-icons/fi";

declare global {
  interface Window {
    instgrm?: {
      Embeds: {
        process: () => void;
      };
    };
  }
}

export default function MediaPage() {
  const [videoDialogOpen, setVideoDialogOpen] = useState(false);
  const [currentVideo, setCurrentVideo] = useState("");
  const [activeTab, setActiveTab] = useState("videos");
  const instagramLoaded = useRef(false);
  
  const openVideoDialog = (videoId: string) => {
    setCurrentVideo(videoId);
    setVideoDialogOpen(true);
  };

  // Handle tab change
  const handleTabChange = (value: string) => {
    setActiveTab(value);
    if (value === 'social') {
      loadInstagram();
    }
  };

  // Load Instagram embed script and process embeds
  const loadInstagram = () => {
    if (!document.getElementById('instagram-embed-script')) {
      const script = document.createElement('script');
      script.id = 'instagram-embed-script';
      script.src = 'https://www.instagram.com/embed.js';
      script.async = true;
      script.onload = () => {
        instagramLoaded.current = true;
        processEmbeds();
      };
      document.body.appendChild(script);
    } else if (window.instgrm) {
      processEmbeds();
    }
  };

  const processEmbeds = () => {
    if (window.instgrm) {
      window.instgrm.Embeds.process();
    }
  };

  // Load Instagram embed script and set up processing
  useEffect(() => {
    // Initial load for Instagram if social tab is active
    if (activeTab === 'social') {
      loadInstagram();
    }

    // Add periodic processing for Instagram embeds when on social tab
    const interval = setInterval(() => {
      if (activeTab === 'social' && window.instgrm) {
        processEmbeds();
      }
    }, 1000);

    return () => {
      clearInterval(interval);
      // Clean up script if needed
      const scriptElement = document.getElementById('instagram-embed-script');
      if (scriptElement && instagramLoaded.current) {
        document.body.removeChild(scriptElement);
      }
    };
  }, [activeTab]);
  
  return (
    <main>
      <h1 className="text-3xl font-bold mb-2">Election News & Media Coverage</h1>
      <h3 className="text-xl mb-6 text-gray-600">
        Stay Informed About the 2025 City Council Elections
      </h3>
      
      <p className="mb-8">
        Watch candidate interviews, read news coverage, and stay up-to-date with the latest election 
        developments from trusted local sources.
      </p>
      
      <Tabs defaultValue="social" className="mb-8" onValueChange={handleTabChange}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="videos">Videos</TabsTrigger>
          <TabsTrigger value="news">News Articles</TabsTrigger>
          <TabsTrigger value="social">Social Media</TabsTrigger>
        </TabsList>
        
        <TabsContent value="videos" className="p-6 bg-white rounded-lg shadow-md mt-2">
          <h3 className="text-xl font-semibold mb-4">Candidate Interviews & Coverage</h3>
          
          <div className="grid md:grid-cols-2 gap-6">
            {/* Video card 1 */}
            <div className="bg-gray-100 rounded-lg overflow-hidden">
              <div className="relative aspect-video">
                <div className="absolute inset-0 flex items-center justify-center bg-gray-700/20 hover:bg-gray-700/30 cursor-pointer transition"
                     onClick={() => openVideoDialog("PxAKOxZk7z4")}>
                  <div className="h-16 w-16 flex items-center justify-center bg-red-600 text-white rounded-full">
                    <FiPlay size={30} />
                  </div>
                </div>
                <img 
                  src="https://img.youtube.com/vi/PxAKOxZk7z4/maxresdefault.jpg" 
                  alt="Chattanooga elections thumbnail" 
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="p-4">
                <h4 className="font-medium text-lg">Chattanooga elections: Who's on the ballot?</h4>
                <p className="text-gray-600">Chattanooga Times Free Press</p>
              </div>
            </div>
            
            {/* Video card 2 */}
            <div className="bg-gray-100 rounded-lg overflow-hidden">
              <div className="relative aspect-video">
                <div className="absolute inset-0 flex items-center justify-center bg-gray-700/20 hover:bg-gray-700/30 cursor-pointer transition"
                     onClick={() => openVideoDialog("x8wwylBLIVE")}>
                  <div className="h-16 w-16 flex items-center justify-center bg-red-600 text-white rounded-full">
                    <FiPlay size={30} />
                  </div>
                </div>
                <img 
                  src="https://img.youtube.com/vi/x8wwylBLIVE/maxresdefault.jpg" 
                  alt="ChattaMatters thumbnail" 
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="p-4">
                <h4 className="font-medium text-lg">City Council Candidate Forum</h4>
                <p className="text-gray-600">ChattaMatters</p>
              </div>
            </div>
          </div>
        </TabsContent>
        
        <TabsContent value="news" className="p-6 bg-white rounded-lg shadow-md mt-2">
          <h3 className="text-xl font-semibold mb-4">Latest News Articles</h3>

          <div className="space-y-6">
            <div className="border-b pb-4">
              <h4 className="font-medium text-lg mb-1">
                <a href="https://chattamatters.com/whos-running-for-mayor-and-city-council-chattanooga-2025/"
                   target="_blank"
                   rel="noopener noreferrer"
                   className="text-blue-700 hover:underline">
                  Who's Running for Mayor and City Council? Chattanooga 2025
                </a>
              </h4>
              <p className="text-gray-600 mb-2">ChattaMatters • January 15, 2025</p>
              <p>A comprehensive guide to all the candidates in the upcoming Chattanooga municipal elections, including backgrounds, platforms, and key issues.</p>
            </div>
          </div>
        </TabsContent>
        
        <TabsContent value="social" className="p-6 bg-white rounded-lg shadow-md mt-2">
          <h3 className="text-xl font-semibold mb-4">Social Media Updates</h3>

          <div className="grid grid-cols-1 md:grid-cols-1 gap-6">
            {/* Instagram Embed - The Chattanooga Show */}
            <div className="bg-white rounded-lg overflow-hidden">
              <div className="instagram-embed-container">
                <blockquote
                  className="instagram-media"
                  data-instgrm-permalink="https://www.instagram.com/reel/DE7SC4JtTrl/"
                  data-instgrm-version="14"
                >
                </blockquote>
              </div>
              {/* Fallback if embed fails */}
              <div className="p-4 text-center">
                <h4 className="font-medium">The Chattanooga Show</h4>
                <p className="text-sm text-gray-500 mb-2">@chattanoogashow</p>
                <a
                  href="https://www.instagram.com/reel/DE7SC4JtTrl/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  View this post on Instagram
                </a>
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>
      
      {/* Video Dialog */}
      <Dialog open={videoDialogOpen} onOpenChange={setVideoDialogOpen}>
        <DialogContent className="max-w-3xl p-0" onInteractOutside={(e) => e.preventDefault()}>
          <div className="aspect-video w-full">
            <iframe 
              width="100%" 
              height="100%" 
              src={`https://www.youtube.com/embed/${currentVideo}`}
              title="YouTube video player" 
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
              allowFullScreen
              className="border-0"
            ></iframe>
          </div>
        </DialogContent>
      </Dialog>
    </main>
  );
} 