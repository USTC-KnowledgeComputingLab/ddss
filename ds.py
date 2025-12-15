import sys
import time
from apyds import Search
from orm import initialize_database, insert_or_ignore, Facts, Ideas
from poly import Poly


def main(addr):
    engine, session = initialize_database(addr)

    search = Search()
    max_fact = -1

    while True:
        begin = time.time()

        with session() as sess:
            for i in sess.query(Facts).filter(Facts.id > max_fact):
                max_fact = max(max_fact, i.id)
                search.add(Poly(dsp=i.data).ds)

            def handler(rule):
                poly = Poly(rule=rule)
                insert_or_ignore(sess, Facts, poly.dsp)
                if idea := poly.idea:
                    insert_or_ignore(sess, Ideas, idea.dsp)
                return False

            count = search.execute(handler)
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
