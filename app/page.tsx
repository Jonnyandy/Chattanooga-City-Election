import DistrictFinder from "@/components/DistrictFinder";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, Button } from "@/components/ui/registry";
import Link from "next/link";

export default function Home() {
  return (
    <main className="pb-12 space-y-12">
      <section>
        <Card className="border-none shadow-lg">
          <CardHeader className="text-center pb-2">
            <CardTitle className="text-4xl font-bold text-blue-800">Find Your Chattanooga City Council District</CardTitle>
            <CardDescription className="text-xl text-gray-600 max-w-3xl mx-auto">
              Discover which district you belong to, who represents you, and where to vote in the March 4th, 2025 election.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <DistrictFinder />
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-500 mb-2">Having trouble with the map above?</p>
              <Link href="/reliable-map" className="text-blue-600 hover:text-blue-800 font-medium">
                Try our alternative map finder →
              </Link>
            </div>
          </CardContent>
        </Card>
      </section>
      
      <section>
        <h2 className="text-3xl font-bold mb-8 text-center">Why Your Vote Matters</h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          <Card className="transition-all hover:shadow-md">
            <CardHeader className="pb-2">
              <CardTitle className="text-xl font-semibold text-blue-700">Local Impact</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                City Council decisions directly affect your daily life - from roads and parks to public safety and neighborhood development.
              </p>
            </CardContent>
          </Card>
          
          <Card className="transition-all hover:shadow-md">
            <CardHeader className="pb-2">
              <CardTitle className="text-xl font-semibold text-blue-700">Every Vote Counts</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Local elections are often decided by small margins. Your single vote has more power in city elections than in any other type.
              </p>
            </CardContent>
          </Card>
          
          <Card className="transition-all hover:shadow-md">
            <CardHeader className="pb-2">
              <CardTitle className="text-xl font-semibold text-blue-700">Community Voice</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Voting gives you a direct say in who represents your neighborhood and how resources are allocated in your community.
              </p>
            </CardContent>
          </Card>
        </div>
        
        <div className="mt-10 text-center">
          <Button asChild className="bg-blue-700 hover:bg-blue-800 text-lg px-6 py-6 h-auto">
            <Link href="/how-to-vote">
              Learn How to Vote →
            </Link>
          </Button>
        </div>
      </section>
    </main>
  );
} 