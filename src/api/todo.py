# Flow Diagram

    # Project Initiation
        # Initialize SQL DB
            # Table 1: **StoredFiles**: Columns (Doc Id(Hashed by doc name)[Primary Key], content hash, doc name)
            # Table 2: **Chunk Store**: Columns (Chunk Id[Primary Key], Doc Id[Foreign Key])
        # Initialize Vector DB

    # Request Hit
        # POST uploadfile/
            # Hash the doc name
            # Search the same in sql db =>  2 Scenarios YES/NO (Drawback: I won't have the older version of the file)
                # Scenario YES
                    # YES : If exists, hash doc content
                    # YES : If matching, then throw error
                    # YES : If not, delete all the chunks for that corresponding doc id
                    # YES : Trigger the new document process
                # # Scenario NO
                    # NO : Trigger the **New Document Process**.    
                    # New Document Process
                        # Hash Document Name
                        # Hash Document Content
                        # Yield to Document Chunking
                        # Yield to Vector Store and get chunk ids
                        # Insert operation to SQL DB Tables
        
        # GET query/{query: string}

        # DELETE delete/{document_name}

        # DELETE reset/

# Drawback/Constraints

    # This set up is designed for one and only 1 user/entity whose docs will be stored in all DB
    # Only markdown file support as of now
    # Document Names cannot be same
    # I am not storing metadata anywhere for efficient searching of document. This will slowdown the searching process.