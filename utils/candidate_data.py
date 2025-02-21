import streamlit as st
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class CandidateContact:
    email: Optional[str] = None
    phone: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None

@dataclass
class Candidate:
    name: str
    district: str
    photo_url: Optional[str] = None
    contact: CandidateContact = None
    bio: Optional[str] = None
    assets_photo: Optional[str] = None

    def __post_init__(self):
        # Check for photo in attached_assets
        if not self.assets_photo:
            name_variants = [
                self.name.replace(' ', '-'),
                self.name.replace(' ', '_'),
                self.name.lower().replace(' ', '-'),
                self.name.lower().replace(' ', '_')
            ]

            for name in name_variants:
                patterns = [
                    f"{name}.avif",
                    f"{name}-District-{self.district}.avif",
                    f"{name}-D{self.district}.avif",
                    f"{name}.jpg"
                ]

                for pattern in patterns:
                    photo_path = Path('attached_assets') / pattern
                    if photo_path.exists():
                        self.assets_photo = str(photo_path)
                        break
                if self.assets_photo:
                    break

# Candidate data
CANDIDATES_2025 = {
    "1": [
        Candidate(
            name="Chip Henderson",
            district="1",
            contact=CandidateContact(
                email="electchiphenderson@gmail.com",
                phone="(423) 821-1331",
                twitter="https://x.com/1chiphenderson",
                facebook="https://www.facebook.com/electchiphenderson/"
            )
        ),
        Candidate(
            name="James \"Skip\" Burnette",
            district="1",
            contact=CandidateContact(
                email="skippythp@comcast.net"
            )
        )
    ],
    "2": [
        Candidate(
            name="Jenny Hill",
            district="2",
            contact=CandidateContact(
                email="jenny@votejennyhill.org",
                phone="(423) 643-7187",
                website="https://www.votejennyhill.org/",
                instagram="https://www.instagram.com/votejennyhill/"
            )
        )
    ],
    "3": [
        Candidate(
            name="Jeff Davis",
            district="3",
            contact=CandidateContact(
                email="team@votejeffdavis.com",
                website="https://votejeffdavis.com/"
            )
        ),
        Candidate(
            name="Tom Marshall",
            district="3",
            contact=CandidateContact(
                email="info@electtommarshall.com",
                phone="(423) 212-3421",
                website="https://electtommarshall.com/"
            )
        )
    ],
    "4": [
        Candidate(
            name="Cody Harvey",
            district="4",
            contact=CandidateContact(
                website="https://cody4council.com/",
                facebook="https://www.facebook.com/cody.harvey.12/",
                linkedin="https://www.linkedin.com/in/cody-harvey-mba-bsn-rn-1b5844145/"
            )
        )
    ],
    "5": [
        Candidate(
            name="Isiah (Ike) Hester",
            district="5",
            contact=CandidateContact(
                facebook="https://www.facebook.com/councilmanhester/",
                instagram="https://www.instagram.com/isiahhester/",
                email="Isiahhester7@gmail.com",
                website="https://www.isiahhester.com/"
            )
        ),
        Candidate(
            name="Dennis Clark",
            district="5",
            contact=CandidateContact(
                website="https://www.dennisclark.org/",
                email="info@dennisclark.org",
                phone="423.255.5683",
                facebook="https://www.facebook.com/VoteDennisClark"
            )
        ),
        Candidate(
            name="Cory Hall",
            district="5",
            contact=CandidateContact(
                facebook="https://www.facebook.com/corydewaynehall/"
            )
        ),
        Candidate(
            name="Samantha Reid-Hawkins",
            district="5",
            contact=CandidateContact(
                facebook="https://www.facebook.com/profile.php?id=100024014033854",
                instagram="https://www.instagram.com/edgbbbhhb"
            )
        )
    ],
    "6": [
        Candidate(
            name="Jenni Berz",
            district="6",
            contact=CandidateContact(
                website="https://jenniberz.com/",
                linkedin="https://www.linkedin.com/in/jenni-berz-933a819/"
            )
        ),
        Candidate(
            name="Jennifer Gregory",
            district="6",
            contact=CandidateContact(
                facebook="https://www.facebook.com/profile.php?id=61570904197451",
                website="https://www.gregoryfor6.com/",
                phone="(423) 355-5735",
                email="gregoryfor6@gmail.com"
            )
        ),
        Candidate(
            name="Mark Holland",
            district="6",
            contact=CandidateContact(
                website="https://markholland.vote/",
                phone="(423) 785-6863"
            )
        ),
        Candidate(
            name="Christian Siler",
            district="6",
            contact=CandidateContact(
                instagram="https://www.instagram.com/christiansiler",
                facebook="https://www.facebook.com/ChristianSilerHomeandLand/",
                email="christiansiler@kw.com"
            )
        ),
        Candidate(
            name="Robert C Wilson",
            district="6"
        )
    ],
    "7": [
        Candidate(
            name="Raquetta Dotley",
            district="7",
            contact=CandidateContact(
                website="https://www.raquettadotley.com/",
                phone="(423) 402-0077",
                email="raquetta@raquettadotley.com",
                facebook="https://www.facebook.com/VoteRaquetta/"
            )
        )
    ],
    "8": [
        Candidate(
            name="Marvene Noel",
            district="8",
            contact=CandidateContact(
                facebook="https://www.facebook.com/CouncilwomanMarveneNoel/",
                phone="(423) 643-7180",
                email="marvene@marvenenoel.com",
                website="https://www.marvenenoel.com/"
            )
        ),
        Candidate(
            name="Anna Golladay",
            district="8",
            contact=CandidateContact(
                website="https://annagolladay.com/",
                phone="423-708-5546",
                email="campaign@annagolladay.com",
                instagram="https://www.instagram.com/unholyhairetic"
            )
        ),
        Candidate(
            name="Doll Sandridge",
            district="8",
            contact=CandidateContact(
                facebook="https://www.facebook.com/p/Doll-Sandridge-For-District-8-61569480122309/",
                phone="423 771 1072",
                email="Dollfordistrict8@gmail.com",
                instagram="https://www.instagram.com/dollfordistrict8"
            )
        ),
        Candidate(
            name="Kelvin Scott",
            district="8",
            contact=CandidateContact(
                facebook="https://www.facebook.com/profile.php?id=61569827262405",
                website="https://www.kelvinscottdistrict8.com/",
                email="citycouncil82024@gmail.com"
            )
        )
    ],
    "9": [
        Candidate(
            name="Ron Elliott",
            district="9",
            contact=CandidateContact(
                website="https://www.ronelliott.com/",
                instagram="https://www.instagram.com/ronelliottchattanooga/",
                email="info@ronelliott.com",
                phone="(423) 708-5546"
            )
        ),
        Candidate(
            name="Letechia Ellis",
            district="9",
            contact=CandidateContact(
                email="letechiaellis@gmail.com",
                phone="(423) 708-5546",
                facebook="https://www.facebook.com/ministerletechia.hymes",
                instagram="@letechiaellis"
            )
        ),
        Candidate(
            name="Evelina Irén Kertay",
            district="9",
            contact=CandidateContact(
                linkedin="https://www.linkedin.com/in/evelina-ir%C3%A9n-kertay-47b44b183/",
                facebook="https://www.facebook.com/p/Evelina-Kertay-for-Chattanooga-City-Council-District-9-61571573788960/",
                email="evelinairenk@gmail.com",
                phone="423-847-5647",
                website="https://evelinairenk.wixsite.com/home"
            )
        )
    ]
}

def get_all_candidates() -> List[Candidate]:
    """Get a flat list of all candidates"""
    candidates = []
    for district_candidates in CANDIDATES_2025.values():
        candidates.extend(district_candidates)
    return candidates

def get_district_candidates(district: str) -> List[Candidate]:
    """Get candidates for a specific district"""
    return CANDIDATES_2025.get(str(district), [])