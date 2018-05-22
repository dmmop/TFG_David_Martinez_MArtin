package es.dmmop;

import com.jayway.jsonpath.PathNotFoundException;

import java.io.*;
import java.net.URL;
import java.util.ArrayList;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.logging.Logger;
import java.util.zip.GZIPInputStream;

import static es.dmmop.Extractor.COMMIT_TYPE;
import static es.dmmop.Extractor.LANG_TYPE;

public class Process extends Thread {
    private static final String OUTPUT_LANG = "git_langs.json";         // Fichero de salida con los lenguages
    private static final String OUTPUT_COMMITS = "git_commits.json";    // Fichero de salida con los commits
    private static final String OUTPUT_ERROR = "git_errors.json";       // Fichero de salida con los errores

    private ArrayList<URL> urls = new ArrayList<>();
    static AtomicInteger processed_links = new AtomicInteger(0);
    private Logger log;
    private Extractor extractor = new Extractor();
    private static PrintWriter out_lang; //Write para usar el disco
    private static PrintWriter out_commit; //Write para usar el disco


    static {
        try {
            out_lang = new PrintWriter(new FileWriter(OUTPUT_LANG, true));
            out_commit = new PrintWriter(new FileWriter(OUTPUT_COMMITS, true));

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void addURLs(URL url) {
        this.urls.add(url);
    }

    @Override
    public void run() {
        System.setProperty("java.util.logging.SimpleFormatter.format",
                "[%1$tF %1$tT] [%4$-7s] %5$s %n");
        log = Logger.getLogger(Thread.currentThread().getName());
        urls.forEach(this::downloadUsingNIO);
    }


    /**
     * Descarga el fichero que contiene la URL y lo descomprime (Presumiblemenente es un .zip)
     *
     * @param url Fichero a descargar
     */
    private void downloadUsingNIO(URL url) {
        String line = "";
        String result[];
        try {
            GZIPInputStream gzip = new GZIPInputStream(url.openStream());
            BufferedReader bf = new BufferedReader(new InputStreamReader(gzip, "UTF-8"));
            while ((line = bf.readLine()) != null) {
                if (line.length() > 0) {
                    result = extractor.extract(line);
                    if (result != null) {
                        if (result[1].equals(String.valueOf(LANG_TYPE))) write_lang(result[0]);
                        else if (result[1].equals(String.valueOf(COMMIT_TYPE))) write_commit(result[0]);
                    }
                }
            }
        } catch (PathNotFoundException e) {
            log.warning("Fallo al encontrar el path: " + line);
            log_error(line);

        } catch (IOException e) {
            log.warning(e.getMessage());
        }
        processed_links.incrementAndGet();
    }

    private synchronized static void write_lang(String result) {
        out_lang.println(result);
    }

    private synchronized static void write_commit(String result) {
        out_commit.println(result);
    }

    private synchronized void log_error(String line) {
        PrintWriter out_error = null;
        try {
            line = line.replaceAll("\n", ""); // Normalizar línea
            out_error = new PrintWriter(new FileWriter(OUTPUT_ERROR, true));
            out_error.println(line);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (out_error != null) out_error.close();
        }
    }

    public static void close_files() {
        out_lang.close();
        out_commit.close();
    }
}
