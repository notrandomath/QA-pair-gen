"""given an entry from Amazon-combined, sample chunks of text"""

from random import sample


class SampleTextChunks:
    def __init__(self):
        self._text_entries = ""

    def _cat(self, entry: dict) -> None:
        """concatenates the text chunks"""
        self._text_entries = ": ".join(entry["description"])
        for review in entry["reviews"]:
            self._text_entries += f": {review['text']}"

    def _chunk(self, n) -> None:
        """chunks the text"""
        self._text_entries = [
            self._text_entries[i : i + n] for i in range(0, len(self._text_entries), n)
        ]

    def get_chunks(self, entry: dict, chunk_size: int = 256) -> list[str]:
        """returns a list of text chunks from a given entry in Amazon-combined"""
        self._cat(entry)
        self._chunk(chunk_size)
        return self._text_entries

    def sample(self, entry: dict, k: int = 3, chunk_size: int = 256) -> list[str]:
        """returns a sample of k text chunks from a given entry in Amazon-combined"""
        if not self._text_entries:
            self.get_chunks(entry, chunk_size)
        if len(self._text_entries) <= k:
            return self._text_entries
        return sample(self._text_entries, k=k)

    def reset(self) -> None:
        """resets the text entries"""
        self._text_entries = ""
