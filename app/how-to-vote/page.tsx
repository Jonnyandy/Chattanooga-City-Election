import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import Link from "next/link";

export default function HowToVotePage() {
  return (
    <main className="pb-12 space-y-10">
      <div className="space-y-2">
        <h1 className="text-4xl font-bold text-blue-800">How to Vote in Chattanooga City Council Elections</h1>
        <p className="text-xl text-gray-600">Complete Guide for Chattanooga Voters</p>
      </div>
      
      <Card className="bg-blue-50 border-blue-200">
        <CardContent className="pt-6">
          <p className="text-blue-800">
            Everything you need to know about voting in the March 4th, 2025 City Council election. 
            Find information about registration, polling locations, and important dates.
          </p>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Important Dates</CardTitle>
          <CardDescription>Mark your calendar with these critical election deadlines</CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="space-y-4">
            <li className="flex items-baseline">
              <Badge variant="default" className="mr-4 bg-blue-600 text-white px-3 py-1 text-sm">Election Day</Badge>
              <span className="text-lg">March 4th, 2025</span>
            </li>
            <li className="flex items-baseline">
              <Badge variant="default" className="mr-4 bg-blue-600 text-white px-3 py-1 text-sm">Early Voting</Badge>
              <span className="text-lg">February 12th - February 27th, 2025</span>
            </li>
            <li className="flex items-baseline">
              <Badge variant="default" className="mr-4 bg-blue-600 text-white px-3 py-1 text-sm">Registration Deadline</Badge>
              <span className="text-lg">February 2nd, 2025</span>
            </li>
          </ul>
        </CardContent>
      </Card>
      
      <Tabs defaultValue="registration" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="registration">Registration</TabsTrigger>
          <TabsTrigger value="locations">Voting Locations</TabsTrigger>
          <TabsTrigger value="id">ID Requirements</TabsTrigger>
        </TabsList>
        
        <TabsContent value="registration">
          <Card>
            <CardHeader>
              <CardTitle>Verify Your Voter Registration</CardTitle>
              <CardDescription>Make sure you're ready to vote in the upcoming election</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p>
                To check if you're registered to vote in the March 4th, 2025 election, visit the official Tennessee voter lookup tool:
              </p>
              <Button asChild className="bg-blue-600 hover:bg-blue-700">
                <a 
                  href="https://tnmap.tn.gov/voterlookup/" 
                  target="_blank" 
                  rel="noopener noreferrer"
                >
                  Verify your registration ↗
                </a>
              </Button>
              
              <div className="pt-4">
                <h4 className="font-semibold text-lg mb-2">Requirements:</h4>
                <ul className="list-disc pl-5 space-y-1">
                  <li>Valid TN Photo ID</li>
                  <li>Must be 18+ by election day</li>
                  <li>Chattanooga resident</li>
                </ul>
              </div>
            </CardContent>
            <CardFooter>
              <p className="font-medium">
                Need to register or update your information?<br />
                Visit <a 
                  href="https://govotetn.gov" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  GoVoteTN.gov
                </a>
              </p>
            </CardFooter>
          </Card>
        </TabsContent>
        
        <TabsContent value="locations">
          <Card>
            <CardHeader>
              <CardTitle>Early Voting Locations</CardTitle>
              <CardDescription>Multiple locations available for your convenience</CardDescription>
            </CardHeader>
            <CardContent>
              <Accordion type="single" collapsible className="w-full">
                <AccordionItem value="item-1">
                  <AccordionTrigger>Election Commission Office</AccordionTrigger>
                  <AccordionContent>
                    <p>700 River Terminal Road</p>
                    <p>Monday - Friday, 8 AM - 6 PM</p>
                    <p>Saturday, 9 AM - 4 PM</p>
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-2">
                  <AccordionTrigger>Brainerd Recreation Center</AccordionTrigger>
                  <AccordionContent>
                    <p>1010 N Moore Road</p>
                    <p>Monday - Friday, 10 AM - 6 PM</p>
                    <p>Saturday, 9 AM - 4 PM</p>
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-3">
                  <AccordionTrigger>Hixson Community Center</AccordionTrigger>
                  <AccordionContent>
                    <p>5401 School Drive</p>
                    <p>Monday - Friday, 10 AM - 6 PM</p>
                    <p>Saturday, 9 AM - 4 PM</p>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
              
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
                <h4 className="font-semibold">Need a Ride?</h4>
                <p>Free rides to polling locations are available. Call (423) 209-8683 for assistance.</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="id">
          <Card>
            <CardHeader>
              <CardTitle>What to Bring</CardTitle>
              <CardDescription>Required identification for voting in Tennessee</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p>You must bring a valid photo ID to vote in Tennessee. Acceptable IDs include:</p>
              
              <ul className="list-disc pl-5 space-y-1">
                <li>Tennessee driver license with your photo</li>
                <li>United States Passport</li>
                <li>Photo ID issued by the Tennessee Department of Safety and Homeland Security</li>
                <li>Photo ID issued by the federal or Tennessee state government</li>
                <li>United States Military photo ID</li>
                <li>Tennessee handgun carry permit with your photo</li>
              </ul>
              
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                <p className="font-medium">
                  <strong>Note:</strong> College student IDs, photo library cards, and photo IDs issued by other states are NOT acceptable.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </main>
  );
} 