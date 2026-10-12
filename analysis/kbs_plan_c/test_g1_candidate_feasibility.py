import unittest
from datetime import datetime,timedelta
from g1_candidate_feasibility import active_author_counts

class ActiveCandidateTests(unittest.TestCase):
    def test_half_open_room_lifecycles_and_author_deduplication(self):
        t=datetime(2026,3,24,12)
        rooms=[
            (t-timedelta(hours=2),t+timedelta(hours=1),10),
            (t-timedelta(hours=1),t+timedelta(hours=2),10),
            (t,t+timedelta(hours=3),11),
            (t+timedelta(hours=1),t+timedelta(hours=3),12)]
        result=active_author_counts(iter(rooms),{10,11,12},
                                    [t,t+timedelta(hours=1)])
        self.assertEqual(result["distinct_known_author_candidate_distribution"]["min"],2)
        self.assertEqual(result["distinct_known_author_candidate_distribution"]["max"],3)
        self.assertEqual(result["known_author_active_room_distribution"]["min"],3)

if __name__=="__main__":
    unittest.main()
