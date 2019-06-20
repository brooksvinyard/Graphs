import random
def fisher_yates_shuffle(l):
    for i in range(0, len(l)):
        random_index = random.randint(0, len(l) - 1)
        l[random_index], l[i] = l[i], l[random_index]

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(numUsers): 
            self.addUser(i)

        # Create friendships
        # make a list of all possible friend combinations
        all_combos = []
        for x in range(1, numUsers + 1):
            for y in range(x, numUsers + 1):
                if x is not y:
                    all_combos.append([x, y])

        # Shuffle the list
        fisher_yates_shuffle(all_combos)

        # The total number of friendships needs to be numUsers * avgFriendships
        total_friendships = numUsers * avgFriendships

        # Narrow the all_combos list to number of total_friendships
        all_combos = all_combos[:total_friendships//2]

        for friend in all_combos:
            self.addFriendship(friend[0], friend[1])

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        # bfs to make sure every path is traced
        
        # Create an empty Queue and enqueue A PATH TO the starting vertex
        q = Queue()
        q.enqueue([userID])
        path = [userID]

        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first PATH
            v = q.dequeue()
            # GRAB THE VERTEX FROM THE END OF THE PATH
            if v[-1] not in visited:
                # Mark it as visited
                visited[v[-1]] = v
                # Then add A PATH TO all of its neighbors to the back of the queue
                for friend in self.friendships[v[-1]]:
                    # Copy the path
                    path = v.copy()
                    # Append friend to the back of the copy
                    path.append(friend)
                    # Enqueue copy
                    q.enqueue(path)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(10, 2)
    print(sg.friendships)
    connections = sg.getAllSocialPaths(1)
    print(connections)