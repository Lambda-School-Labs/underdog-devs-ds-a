from random import sample, choice
from typing import List, Tuple, Dict

from app.data import MongoDB
from app.utilities import dict_to_str


class MatcherSort:
    """Callable matching class implemeting simple sorting algorithm.
    
     
    Organizes mentors based on mentee's subject of interest and
    their self-defined skill level, corresponding to mentors'
    teachable subjects and desired skill level(s) to teach.

    Args:
        n_matches (int): Number of mentor matches desired
        mentee_id (int): ID number of mentee that needs mentor
    
    Returns:
        List of mentor IDs
    """
    db = MongoDB("UnderdogDevs")

    def __call__(self, n_matches: int, profile_id: int) -> List[int]:
        """Return a list of matched mentor id numbers."""
        mentee = self.db.first("Mentees", {"profile_id": profile_id})

        def sort_mentors(mentor: Dict) -> Tuple:
            """Sorts mentors """
            return (
                mentee["subject"] != mentor["subject"],
                mentee["experience_level"] != mentor["experience_level"],
            )

        results = sorted(self.db.read("Mentors"), key=sort_mentors)[:n_matches]
        return [mentor["profile_id"] for mentor in results]


class MatcherSearch:
    """Callable matching class implementing simple searching algorithm.
        
    Searches for mentors in database that match the given mentee's
    subject. Note that n_matches is a maximum for the number of
    mentors returned, not a guaranteed count.

    Args:
        n_matches (int): Number of mentor matches desired
        mentee_id (int): ID number of mentee that needs mentor
    
    Returns:
        List of mentor IDs
    """
    db = MongoDB("UnderdogDevs")

    def __call__(self, n_matches: int, profile_id: int) -> List[int]:
        """Return a list of matched mentor id numbers."""
        mentee = self.db.first("Mentees", {"profile_id": profile_id})
        results = self.db.search("Mentors", mentee["subject"])[:n_matches]
        return [mentor["profile_id"] for mentor in results]


class MatcherSortSearch:
    """Callable matching class implementing simple sort-search algorithm.
        
    Searches for mentors in database that match the given mentee's
    subject, and then organizes subsequent mentors based on
    mentee's subject of interest and their self-defined skill
    level, corresponding to mentors' teachable subjects and desired
    skill level(s) to teach.

    Args:
        n_matches (int): Number of mentor matches desired
        mentee_id (int): ID number of mentee that needs mentor
    
    Returns:
        List of mentor IDs
    """
    db = MongoDB("UnderdogDevs")

    def __call__(self, n_matches: int, profile_id: int) -> List[int]:
        """Return a list of matched mentor id numbers."""
        mentee = self.db.first("Mentees", {"profile_id": profile_id})

        def sort_mentors(mentor: Dict) -> Tuple:
            # Todo: Double Check Logic!!!
            return (
                mentee["subject"] != mentor["subject"],
                mentee["experience_level"] != mentor["experience_level"],
                mentee["pair_programming"] != mentor["pair_programming"],
                mentor["industry_knowledge"],
            )

        results = sorted(
            self.db.search("Mentors", mentee["subject"]),
            key=sort_mentors,
        )[:n_matches]
        return [mentor["profile_id"] for mentor in results]


class MatcherRandom:
    """Callable matching class returning random matches.
        
    Randomly samples the mentor database for n_matches number of
    mentors. Note that this function ignores mentee data, and the
    matches are simply random samples of mentors.

    Args:
        n_matches (int): Number of mentor matches desired
        mentee_id (int) (unused): ID number of mentee needing match
    
    Returns:
        List of mentor IDs
    """
    db = MongoDB("UnderdogDevs")

    def __call__(self, n_matches: int, profile_id: int) -> List[int]:
        """Return a list of matched mentor id numbers."""
        results = sample(self.db.read("Mentors"), k=n_matches)
        return [mentor["profile_id"] for mentor in results]


if __name__ == '__main__':
    matcher = MatcherSortSearch()

    db = matcher.db
    mentees = db.read("Mentees")
    test_user_id = choice(mentees)["profile_id"]
    matches = matcher(3, test_user_id)

    print(f"Mentee: {test_user_id}")
    print(f"Matches: {matches}")

    print(dict_to_str(db.first("Mentees", {"profile_id": test_user_id})))
    for mentor_id in matches:
        print(dict_to_str(db.first("Mentors", {"profile_id": mentor_id})))
