def test_get_db_yields_and_closes_session(monkeypatch):
    import database

    class FakeSession:
        closed = False

        def close(self):
            self.closed = True

    fake_session = FakeSession()
    monkeypatch.setattr(database, "SessionLocal", lambda: fake_session)

    generator = database.get_db()
    yielded_session = next(generator)

    assert yielded_session is fake_session

    generator.close()
    assert fake_session.closed is True
