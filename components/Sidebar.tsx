"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { 
  FiMenu, 
  FiX, 
  FiUsers, 
  FiCheckSquare, 
  FiVideo,
  FiMapPin, 
  FiExternalLink, 
  FiInfo
} from "react-icons/fi";
import { useSidebar } from "./SidebarContext";
import {
  Button,
  Separator,
  Sheet,
  SheetContent,
  SheetTrigger,
  Badge
} from "@/components/ui/registry";

type NavLink = {
  href: string;
  label: string;
  icon: React.ReactNode;
  badge?: string;
};

export default function Sidebar() {
  const { toggleSidebar, closeSidebar } = useSidebar();
  const pathname = usePathname();
  const [mounted, setMounted] = useState(false);
  
  // Wait until after client-side hydration to show
  useEffect(() => {
    setMounted(true);
  }, []);
  
  const navLinks: NavLink[] = [
    {
      href: "/",
      label: "Find Your District",
      icon: <FiMapPin className="mr-3" size={20} />
    },
    {
      href: "/candidates",
      label: "Candidates",
      icon: <FiUsers className="mr-3" size={20} />
    },
    {
      href: "/how-to-vote",
      label: "How to Vote",
      icon: <FiCheckSquare className="mr-3" size={20} />
    },
    {
      href: "/media",
      label: "Media",
      icon: <FiVideo className="mr-3" size={20} />
    },
    {
      href: "/election-info",
      label: "Election Info",
      icon: <FiInfo className="mr-3" size={20} />
    }
  ];
  
  const externalLinks = [
    {
      href: "https://www.hamiltontn.gov/election",
      label: "Hamilton County Election Commission",
      icon: <FiExternalLink className="mr-3" size={18} />
    },
    {
      href: "https://www.chattanooga.gov/city-council",
      label: "Current City Council",
      icon: <FiExternalLink className="mr-3" size={18} />
    }
  ];
  
  if (!mounted) return null;
  
  return (
    <>
      {/* Mobile sidebar toggle */}
      <div className="lg:hidden fixed top-4 left-4 z-30">
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="outline" size="icon" className="rounded-full bg-white shadow-md">
              <FiMenu size={20} />
              <span className="sr-only">Toggle menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-[300px] p-0">
            <div className="flex flex-col h-full">
              <div className="p-4 flex items-center justify-between border-b">
                <Link href="/" className="flex items-center" onClick={closeSidebar}>
                  <div className="flex items-center justify-center h-8 w-8 mr-2 bg-blue-600 text-white rounded-md">
                    <FiCheckSquare size={20} />
                  </div>
                  <span className="font-bold text-xl">Chattanooga.Vote</span>
                </Link>
              </div>
              
              <nav className="flex-1 overflow-y-auto p-4">
                <ul className="space-y-2">
                  {navLinks.map((link) => (
                    <li key={link.href}>
                      <Link 
                        href={link.href}
                        onClick={closeSidebar}
                        className={`flex items-center py-2 px-3 rounded-md transition-colors ${
                          pathname === link.href 
                            ? 'bg-blue-100 text-blue-800 font-medium' 
                            : 'text-gray-700 hover:bg-gray-100'
                        }`}
                      >
                        {link.icon}
                        <span>{link.label}</span>
                        {link.badge && (
                          <Badge variant="outline" className="ml-auto">
                            {link.badge}
                          </Badge>
                        )}
                      </Link>
                    </li>
                  ))}
                </ul>
                
                <Separator className="my-4" />
                
                <div className="mb-2 text-sm font-medium text-gray-500 px-3">External Resources</div>
                <ul className="space-y-2">
                  {externalLinks.map((link) => (
                    <li key={link.href}>
                      <a 
                        href={link.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center py-2 px-3 rounded-md text-gray-700 hover:bg-gray-100 transition-colors"
                      >
                        {link.icon}
                        <span className="text-sm">{link.label}</span>
                      </a>
                    </li>
                  ))}
                </ul>
              </nav>
              
              <div className="p-4 border-t">
                <div className="text-sm text-gray-500 mb-2">Election Day</div>
                <div className="font-medium mb-4">March 4th, 2025</div>
                
                {/* Partner Logos */}
                <div className="relative w-full">
                  <Image
                    src="/images/candidates-info.png"
                    alt="Partner Organizations"
                    width={240}
                    height={120}
                    className="w-full h-auto"
                    priority={false}
                  />
                </div>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </div>
      
      {/* Desktop sidebar */}
      <div className="hidden lg:block fixed inset-y-0 left-0 z-20 w-64 bg-white border-r border-gray-200">
        <div className="flex flex-col h-full">
          <div className="p-4 flex items-center border-b">
            <Link href="/" className="flex items-center">
              <div className="flex items-center justify-center h-8 w-8 mr-2 bg-blue-600 text-white rounded-md">
                <FiCheckSquare size={20} />
              </div>
              <span className="font-bold text-xl">Chattanooga.Vote</span>
            </Link>
            
            <Button 
              variant="ghost" 
              size="icon" 
              className="ml-auto lg:hidden"
              onClick={toggleSidebar}
            >
              <FiX size={20} />
              <span className="sr-only">Close sidebar</span>
            </Button>
          </div>
          
          <nav className="flex-1 overflow-y-auto p-4">
            <ul className="space-y-2">
              {navLinks.map((link) => (
                <li key={link.href}>
                  <Link 
                    href={link.href}
                    className={`flex items-center py-2 px-3 rounded-md transition-colors ${
                      pathname === link.href 
                        ? 'bg-blue-100 text-blue-800 font-medium' 
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    {link.icon}
                    <span>{link.label}</span>
                    {link.badge && (
                      <Badge variant="outline" className="ml-auto">
                        {link.badge}
                      </Badge>
                    )}
                  </Link>
                </li>
              ))}
            </ul>
            
            <Separator className="my-4" />
            
            <div className="mb-2 text-sm font-medium text-gray-500 px-3">External Resources</div>
            <ul className="space-y-2">
              {externalLinks.map((link) => (
                <li key={link.href}>
                  <a 
                    href={link.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center py-2 px-3 rounded-md text-gray-700 hover:bg-gray-100 transition-colors"
                  >
                    {link.icon}
                    <span className="text-sm">{link.label}</span>
                  </a>
                </li>
              ))}
            </ul>
          </nav>
          
          <div className="p-4 border-t">
            <div className="text-sm text-gray-500 mb-2">Election Day</div>
            <div className="font-medium mb-4">March 4th, 2025</div>
            
            {/* Partner Logos */}
            <div className="relative w-full">
              <Image
                src="/images/candidates-info.png"
                alt="Partner Organizations"
                width={240}
                height={120}
                className="w-full h-auto"
                priority={false}
              />
            </div>
          </div>
        </div>
      </div>
      
    </>
  );
} 