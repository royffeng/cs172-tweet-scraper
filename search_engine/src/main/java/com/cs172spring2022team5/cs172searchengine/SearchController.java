package com.cs172spring2022team5.cs172searchengine;

import org.springframework.web.bind.annotation.*;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.json.JSONObject;
import java.io.*;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin("*")
public class SearchController {
    public static final String output_directory = "C:/Users/micha/Desktop/cs172-search-engine/cs172-search-engine/index";
    public static Analyzer analyzer = new StandardAnalyzer(); // converts text to tokens

    static {
        File fileCheck = new File(output_directory);
        if (!fileCheck.isDirectory()) {
            try {
                createIndex();
            } catch (Exception e) {
                System.out.println("I died because of: " + e);
            }
        }
    }

    public static void createIndex() throws Exception {
        File inputFile = new File("C:/Users/micha/Desktop/cs172-search-engine/cs172-search-engine/pretty_tweet_collection.json"); // file that you are reading from
        BufferedReader reader = new BufferedReader(new FileReader(inputFile));
        ArrayList<JSONObject> jsonObjectArray = new ArrayList<>();

        Directory index = FSDirectory.open(Paths.get(output_directory)); // stores indexes

        IndexWriterConfig config = new IndexWriterConfig(analyzer); // config that writer uses for analyzing
        IndexWriter indexWriter = new IndexWriter(index, config); // writes the documents to the index

        int errors = 0;
        int runCounter = 0;
        int counter = 0;
        for (String line; (line = reader.readLine()) != null; ) {
            try {
                jsonObjectArray.add(new JSONObject(line));
                counter++;
                if (counter > 1000) {
                    runCounter += counter;
                    indexDocuments(indexWriter, jsonObjectArray);
                    counter = 0;
                    jsonObjectArray.clear();
                    System.out.println(runCounter);
                }
            } catch (Exception e) {
                System.out.println("I died because of: " + e);
                errors++;
            }
        }
        if (counter > 0) {
            runCounter+= counter;
            indexDocuments(indexWriter, jsonObjectArray);
            jsonObjectArray.clear();
            System.out.println(runCounter);
        }
        indexWriter.close();
    }

    public static void indexDocuments(IndexWriter indexWriter, ArrayList<JSONObject> jsonObjectArray) throws IOException {
        // int objCount = 0;
        for (JSONObject element : jsonObjectArray) {
            // objCount++;
            JSONObject id_object = element.getJSONObject("id");
            String id = id_object.getString("$numberLong"); //store as long maybe?
            String tweet_text = element.getString("tweet_text");
            String created_at = element.getString("created_at");
            String name = element.getString("name");
            String screen_name = element.getString("screen_name");

            Document doc;
            doc = new Document();
            doc.add(new TextField("id", id, org.apache.lucene.document.Field.Store.YES)); // technically should be able to import this statement but it's not working
            doc.add(new TextField("tweet_text", tweet_text, org.apache.lucene.document.Field.Store.YES));
            doc.add(new TextField("created_at", created_at, org.apache.lucene.document.Field.Store.YES));
            doc.add(new TextField("name", name, org.apache.lucene.document.Field.Store.YES));
            doc.add(new TextField("screen_name", screen_name, org.apache.lucene.document.Field.Store.YES)); // org.apache.lucene.document.Field.Index.ANALYZED
            indexWriter.addDocument(doc);
        }
        // System.out.println("Total Objects: " + objCount);
    }

    @GetMapping("/search")
    public static List<Document> searchFiles(@RequestParam(required=false, defaultValue="") String queryString) {
        try {
            Query query = new QueryParser("tweet_text", analyzer).parse(queryString);

            Directory indexDirectory = FSDirectory.open(Paths.get(output_directory));
            IndexReader indexReader = DirectoryReader.open(indexDirectory);

            IndexSearcher searcher = new IndexSearcher(indexReader);
            TopDocs topDocs = searcher.search(query, 10);

            // System.out.println("Number of hits: " + topDocs.totalHits);

            List<Document> documents = new ArrayList<>();
            for (ScoreDoc scoreDoc : topDocs.scoreDocs) {
                documents.add(searcher.doc(scoreDoc.doc));
            }

            return documents;
        } catch (Exception e) {
            System.out.println("rip " + e);
            e.printStackTrace();
        }
        return null;
    }
}
