import sys
from orm import initialize_database, insert_or_ignore, Facts, Ideas
from poly import Poly


def main(addr):
    engine, session = initialize_database(addr)

    while True:
        data = input()
        with session() as sess:
            poly = Poly(dsp=data)
            insert_or_ignore(sess, Facts, poly.dsp)
            if idea := poly.idea:
                insert_or_ignore(sess, Ideas, idea.dsp)
            sess.commit()

    engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <database-addr>")
        sys.exit(1)
    main(sys.argv[1])
