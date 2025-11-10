import { FiMapPin, FiUser } from "react-icons/fi";

type DistrictInfoProps = {
  districtInfo: {
    district_number: string;
    precinct: string;
    polling_place: string;
    polling_address: string;
    candidates: string[];
  };
};

export default function DistrictInfo({ districtInfo }: DistrictInfoProps) {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-4">
          Your district is District {districtInfo.district_number}
        </h2>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h3 className="text-xl font-semibold mb-3">Current Council Member</h3>
          <div className="flex items-center">
            <FiUser className="text-blue-600 mr-2" size={20} />
            <span className="font-medium">John Doe</span> {/* This would be dynamic data */}
          </div>
        </div>
      </div>
      
      <div>
        <h3 className="text-xl font-semibold mb-4">March 4th, 2025 Election Candidates</h3>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {districtInfo.candidates.map((candidate, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="p-4">
                <h4 className="text-lg font-semibold text-blue-700">{candidate}</h4>
                
                {/* This would be replaced with dynamic data from your API */}
                <div className="mt-3">
                  <a 
                    href="#" 
                    className="text-blue-600 hover:underline"
                  >
                    Campaign Website
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {districtInfo.polling_place !== "Not found" && (
        <div>
          <h3 className="text-xl font-semibold mb-4">
            <FiMapPin className="inline-block mr-2" /> Your Polling Location
          </h3>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="mb-2">
              <strong>Location:</strong> {districtInfo.polling_place}
            </p>
            <p className="mb-2">
              <strong>Address:</strong> {districtInfo.polling_address}
            </p>
            <p>
              <strong>Precinct:</strong> {districtInfo.precinct}
            </p>
          </div>
        </div>
      )}
    </div>
  );
} 