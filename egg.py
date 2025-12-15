import sys
import time
from orm import initialize_database, insert_or_ignore, Facts, Ideas
from egraph import Search


def main(addr):
    engine, session = initialize_database(addr)

    search = Search()
    pool = []
    max_fact = -1
    max_idea = -1

    while True:
        count = 0
        begin = time.time()
        with session() as sess:
            query = sess.query(Facts).filter(Facts.id > max_fact)
            for i in query:
                max_fact = max(max_fact, i.id)
                search.add(i.data)
            query = sess.query(Ideas).filter(Ideas.id > max_idea)
            for i in query:
                max_idea = max(max_idea, i.id)
                pool.append(i.data)
            for i in pool:
                for o in search.execute(i):
                    insert_or_ignore(sess, Facts, o)
            sess.commit()

        end = time.time()
        duration = end - begin
        if count == 0:
            delay = max(0, 1 - duration)
            time.sleep(delay)

    engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <database-addr>")
        sys.exit(1)
    main(sys.argv[1])
