import CandidatesList from "@/components/CandidatesList";
import { Separator } from "@/components/ui/separator";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function CandidatesPage() {
  return (
    <main className="pb-12 space-y-10">
      <div className="space-y-2">
        <h1 className="text-4xl font-bold text-blue-800">🗳️ Chattanooga Election Candidates</h1>
        <p className="text-xl text-gray-600">March 4th, 2025 Election</p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-blue-700">Mayoral Candidates</CardTitle>
          <CardDescription>
            Meet the candidates running for Mayor of Chattanooga in the upcoming election.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <CandidatesList district="Mayor" />
        </CardContent>
      </Card>
      
      <Separator className="my-8" />
      
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-blue-700">City Council Candidates</CardTitle>
          <CardDescription>
            Meet the candidates running for Chattanooga City Council. Learn about their platforms, 
            experience, and vision for our city. Browse by district or view all candidates.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <CandidatesList district="All" />
        </CardContent>
      </Card>
    </main>
  );
} 