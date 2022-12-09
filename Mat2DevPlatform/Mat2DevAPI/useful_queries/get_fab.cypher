MATCH (u:User) WHERE u.name IN {users}
MATCH (c:Conversation)
  WHERE ALL( x IN collect(u) WHERE (x)-[:IN_CONVERSATION]->(c) )
RETURN c

MATCH(n:Manufacturing),
     (m)-[]-(o)-[]-(n) Return n,m,o
Limit 1