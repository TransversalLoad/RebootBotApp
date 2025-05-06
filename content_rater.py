class ContentRater:
    TOXIC_WORDS = ['rape', 'genocide', 'nazi', 'terrorist'] # add any other ptoentially toxic language here for filtering
    
    def rate_content(self, text):
        toxic_count = sum(text.lower().count(word) for word in self.TOXIC_WORDS)
        
        if toxic_count > 1:
            return "R (Restricted)"
        elif toxic_count > 0:
            return "PG-13"
        else:
            return "PG"