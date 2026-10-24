import collections

class CC1Ledger:
    def __init__(self):
        self.events = []
        self.knowledge_depth = collections.defaultdict(int) # recipe_id -> depth

    def record(self, tick, recipe_id, agent_id, method, teacher_id=None, bio_gen=None):
        # Calculate transmission depth
        depth = 0
        if method in ("taught", "copied") and teacher_id is not None:
            # Depth is 1 + the depth of the teacher for this specific recipe
            # We need to look back in the events to find the teacher's acquisition depth
            teacher_depth = self._get_agent_depth(teacher_id, recipe_id)
            depth = teacher_depth + 1
        
        self.events.append({
            "tick": tick,
            "recipe_id": recipe_id,
            "agent_id": agent_id,
            "method": method,
            "teacher_id": teacher_id,
            "bio_gen": bio_gen,
            "depth": depth
        })
        self.knowledge_depth[(agent_id, recipe_id)] = depth

    def record_use(self, tick, recipe_id, agent_id):
        self.events.append({
            "tick": tick,
            "recipe_id": recipe_id,
            "agent_id": agent_id,
            "method": "used",
            "teacher_id": None,
            "bio_gen": None,
            "depth": None
        })

    def record_forget(self, tick, recipe_id, agent_id):
        self.events.append({
            "tick": tick,
            "recipe_id": recipe_id,
            "agent_id": agent_id,
            "method": "forgot",
            "teacher_id": None,
            "bio_gen": None,
            "depth": None
        })

    def _get_agent_depth(self, agent_id, recipe_id):
        # Search backwards for the most recent acquisition by this agent
        for event in reversed(self.events):
            if event["agent_id"] == agent_id and event["recipe_id"] == recipe_id and event["method"] in ("made", "taught", "copied"):
                return event["depth"]
        return 0

# Singleton instance to be attached to the world
ledger = CC1Ledger()
