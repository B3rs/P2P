__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

class FilesManager(object):

    # @returns array with matches path
    @classmethod
    def find_files_by_query(cls, query, shared_path = '.'):
        # Loop in the shared files directory and look for occurrence
        matches = []

        for dirname, dirnames, filenames in os.walk(shared_path):
            for filename in filenames:
                if filename.lower().find(query.lower()) != -1:
                    matches.append(os.path.join(dirname, filename))

        return matches
