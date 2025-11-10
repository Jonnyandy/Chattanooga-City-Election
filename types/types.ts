export interface Candidate {
  name: string;
  district: string;
}

export interface CouncilMember {
  name: string;
  district: string;
  contact: string;
  email: string;
  status?: string;
  note?: string;
} 