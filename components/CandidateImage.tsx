"use client";

import { useState, useEffect } from 'react';
import Image from 'next/image';

type CandidateImageProps = {
  src: string;
  alt: string;
  className?: string;
};

export default function CandidateImage({ src, alt, className = "" }: CandidateImageProps) {
  const [imgSrc, setImgSrc] = useState<string | null>(null);
  const [error, setError] = useState(false);
  const [useDirectImg, setUseDirectImg] = useState(false);
  
  // Fix common issues with image paths
  const sanitizeImagePath = (path: string): string => {
    // Ensure path starts with /images for candidate photos
    if (path.includes('candidate_photos') && !path.includes('/images/')) {
      path = path.replace('/candidate_photos', '/images/candidate_photos');
    }
    
    // Handle special characters in filenames
    if (path.includes('(') || path.includes(')')) {
      // Replace parentheses with their encoded versions
      path = path.replace(/\(/g, '%28').replace(/\)/g, '%29');
    }
    
    // Handle accented characters
    if (path.includes('é') || path.includes('Irén')) {
      // Try non-accented version as fallback
      const nonAccentedPath = path.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      console.log(`Path contains accents, trying non-accented version: ${nonAccentedPath}`);
      return nonAccentedPath;
    }
    
    // Handle spaces in filenames
    if (path.includes(' ')) {
      // Try an alternate filename format without spaces
      const parts = path.split('/');
      const filename = parts[parts.length - 1];
      const directory = parts.slice(0, parts.length - 1).join('/');
      
      // Check if this is likely a candidate photo
      if (path.includes('candidate_photos')) {
        // Try filename with underscores instead of spaces
        const underscoredFilename = filename.replace(/\s+/g, '_');
        path = `${directory}/${underscoredFilename}`;
      }
    }
    
    return path;
  };
  
  // Try to load the image on component mount
  useEffect(() => {
    // Reset state on src change
    setError(false);
    setUseDirectImg(false);
    
    if (!src) {
      setError(true);
      return;
    }
    
    // Clean up the path
    let processedSrc = sanitizeImagePath(src);
    
    // If src doesn't start with http, assume it's a local path and check if it exists
    if (!processedSrc.startsWith('http')) {
      // Set the image source with cache busting query param
      setImgSrc(`${processedSrc}?t=${new Date().getTime()}`);
    } else {
      setImgSrc(processedSrc);
    }
    
    // Log for debugging
    console.log(`Trying to load image: ${processedSrc} (original: ${src})`);
  }, [src]);
  
  const handleError = () => {
    console.error(`Failed to load image with Next/Image: ${imgSrc}`);
    
    // Try direct img tag as fallback
    if (!useDirectImg) {
      setUseDirectImg(true);
      return;
    }
    
    // If direct img also fails, try alternate file extensions
    if (imgSrc && !error) {
      // Try known file extensions available in the candidate_photos folder
      if (imgSrc.endsWith('.jpg')) {
        // Try png format
        setImgSrc(imgSrc.replace('.jpg', '.png'));
        return;
      } else if (imgSrc.endsWith('.png')) {
        // Try jpg format
        setImgSrc(imgSrc.replace('.png', '.jpg'));
        return;
      } else if (imgSrc.endsWith('.jpeg')) {
        // Try jpg format
        setImgSrc(imgSrc.replace('.jpeg', '.jpg'));
        return;
      } else if (imgSrc.endsWith('.webp')) {
        // Try jpg format
        setImgSrc(imgSrc.replace('.webp', '.jpg'));
        return;
      }
      
      // Try alternate file name formats
      if (imgSrc.includes('Irén')) {
        setImgSrc(imgSrc.replace('Irén', 'Iren'));
        return;
      }
      
      if (imgSrc.includes('(Ike)')) {
        setImgSrc(imgSrc.replace('(Ike)', 'Ike'));
        return;
      }
    }
    
    // If all fallbacks fail, show error state
    setError(true);
  };
  
  if (error || !imgSrc) {
    return (
      <div className={`h-full w-full flex items-center justify-center bg-gray-100 ${className}`}>
        <span className="text-center text-gray-400">No photo available</span>
      </div>
    );
  }
  
  // If Next.js Image failed, try direct img tag
  if (useDirectImg) {
    return (
      <div className="relative h-full w-full">
        <img
          src={imgSrc}
          alt={alt}
          className={`object-cover object-top w-full h-full ${className}`}
          onError={handleError}
        />
      </div>
    );
  }
  
  return (
    <div className="relative h-full w-full">
      <Image
        src={imgSrc}
        alt={alt}
        fill
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        className={`object-cover object-top ${className}`}
        onError={handleError}
        unoptimized={true}
        priority={true}
      />
    </div>
  );
} 