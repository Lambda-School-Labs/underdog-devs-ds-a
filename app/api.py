from typing import Dict, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data import MongoDB
from app.functions import *
from app.model import MatcherSortSearch

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.43.8",
    docs_url='/',
)

API.db = MongoDB("UnderdogDevs")
API.matcher = MatcherSortSearch()

API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/version")
async def version():
    """Return the current version of the API."""
    return {"result": API.version}


@API.get("/collections")
async def collections():
    """Return collection names and a count of their child nodes."""
    return {"result": API.db.get_database_info()()}


@API.post("/{collection}/create")
async def create(collection: str, data: Dict):
    """Create a new record in the given collection.
    
    Creates new document within given collection using the data
    parameter to populate its fields.
    
    Args:
        collection (str): Name of collection retrieved from URL
        data (dict): Key value pairs to be mapped to document fields
        
        Input Example:
        collection = "Mentees"
        data = {
            "profile_id": "test001",
            "first_name": "Luca",
            "last_name": "Evans",
            "email": "fake@email.com",
            "city": "Ashland",
            "state": "Oregon",
            "country": "USA",
            "formerly_incarcerated": true,
            "underrepresented_group": true,
            "low_income": true,
            "list_convictions": [
            "Infraction",
            "Felony"
            ],
            "subject": "Web: HTML, CSS, JavaScript",
            "experience_level": "Beginner",
            "job_help": false,
            "industry_knowledge": false,
            "pair_programming": true,
            "other_info": "Notes"
        }
    
    Returns:
        New collection's data as dictionary
    """
    return {"result": API.db.create(collection, data)}


@API.post("/{collection}/read")
async def read(collection: str, data: Optional[Dict] = None):
    """Return array of records that exactly match the given query.
    
    Defines collection from URL and queries it with optional filters
    given (data). If no filtering data is given, will return all
    documents within collection.
    
    Args:
        collection (str): Name of collection retrieved from URL
        data (dict) (optional): Key value pairs to match
    
    Returns:
        List of all matching documents
    """
    return {"result": API.db.read(collection, data)}


@API.post("/{collection}/update")
async def update(collection: str, query: Dict, update_data: Dict):
    """Update collection and return the number of updated documents.
    
    Defines collection from URL and queries it with filters
    given (query). Then updates fields using update_data, either adding
    or overwriting data.
    
    Args:
        collection (str): Name of collection retrieved from URL
        query (dict): Key value pairs to filter for
        update_data (dict): Key value pairs to update
    
    Returns:
        Integer count of updated documents
    """
    return {"result": API.db.update(collection, query, update_data)}


@API.post("/{collection}/search")
async def collection_search(collection: str, search: str):
    """Return list of docs loosely matching string, sorted by relevance.
    
    Searches collection given in URL for documents that approximate the
    given string (search), and then presents them, automatically
    ordering results by relevance to the search.
    
    Args:
        collection (str): Name of collection to query
        search (str): Querying parameter
    
    Returns:
        List of queried documents
        """
    return {"result": API.db.search(collection, search)}


@API.post("/match/{profile_id}")
async def match(profile_id: str, n_matches: int):
    """Return an array of mentor matches for any given mentee profile_id.
    
    Utilizes imported MatcherSortSearch() to query database for the
    given number of mentors that may be a good match for the given
    mentee. See documentation for MatcherSortSearch() for details.
    
    Args:
        profile_id (str): ID number for mentee needing a mentor
        n_matches (int): Maximum desired matching candidates
        
    Returns:
        List of mentor IDs
    """
    return {"result": API.matcher(n_matches, profile_id)}


@API.delete("/{collection}/delete/{profile_id}")
async def delete(collection: str, profile_id: str):
    """Removes a user from the given collection.

    Deletes all documents containing the given profile_id permanently,
    and returns the deleted profile_id for confirmation.

    Args:
        collection (str): Name of collection to query for deletion
        profile_id (str): ID number of user to be deleted
    
    Returns:
        Dictionary with key of "deleted" and value of the profile_id
    """
    API.db.delete(collection, {"profile_id": profile_id})
    return {"result": {"deleted": profile_id}}

@API.post("/financial_aid/{profile_id}")
async def financial_aid(profile_id: str):
    """Returns the the probability that financial aid will be required.
    
    Calls a the financial aid function from functions.py inputing the 
    profile_id for calculation involving formally incarcerated, low income,
    and experience level as variables to formulate probability of financial aid
    
    Args:
        profile_id (str): the profile id of the mentee
    
    Returns:
        the the probability that financial aid will be required
        """
    return {"result": await financial_aid(profile_id)}
