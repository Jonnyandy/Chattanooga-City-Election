import DistrictFinder from "@/components/DistrictFinder";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function ReliableMapPage() {
  return (
    <main className="pb-12 space-y-12">
      <section>
        <Card className="border-none shadow-lg">
          <CardHeader className="text-center pb-2">
            <CardTitle className="text-4xl font-bold text-blue-800">Alternative District Finder</CardTitle>
            <CardDescription className="text-xl text-gray-600 max-w-3xl mx-auto">
              This page provides the same district finder functionality as the main page.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <DistrictFinder />
          </CardContent>
        </Card>
      </section>
    </main>
  );
} 