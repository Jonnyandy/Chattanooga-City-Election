import { Inter } from "next/font/google";
import "./globals.css";
import { SidebarProvider } from "@/components/SidebarContext";
import Sidebar from "@/components/Sidebar";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Chattanooga City Election",
  description: "Find your district, learn about candidates, and get voting information for the Chattanooga City Council Election.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn(
        inter.className,
        "min-h-screen bg-background font-sans antialiased"
      )}>
        <SidebarProvider>
          <div className="relative min-h-screen bg-background">
            <Sidebar />
            <div className="lg:pl-64 transition-all duration-300">
              <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
                {children}
              </div>
            </div>
          </div>
        </SidebarProvider>
      </body>
    </html>
  );
} 