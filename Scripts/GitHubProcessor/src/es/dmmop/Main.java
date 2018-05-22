package es.dmmop;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;

public class Main {
    private static final int HILOS = 16;
    // URL sobre la que se construye la petición (año, mes, dia y hora)
    private static final String URL_BASE = "http://data.githubarchive.org/20%d-%02d-%02d-%02d.json.gz";

    //Lista con todos los hilos que se van a lanzar
    private static final ArrayList<Process> process_list = new ArrayList<>();

    public static void main(String[] args) {
        long start = System.nanoTime();
        create_balance_threads();
        launch_threads();
        long time = System.nanoTime() - start;
        System.out.printf("Took %.3f seconds", time / 1e9);
    }

    /**
     * Genera un número de hilos y distribuye uniformemente los ficheros que se descargarán
     */
    private static void create_balance_threads(){
        int balanced = 0;
        for (int i = 0; i < HILOS; i++) process_list.add(new Process());
        URL url;
            for (int anno = 15; anno <= 17; anno++) {
                for (int mes = 1; mes <= 12; mes++) {
                    for (int dia = 1; dia <= 31; dia++) {
                        for (int hora = 0; hora < 24; hora++) {
                            try {
                                url = new URL(String.format(URL_BASE, anno, mes, dia, hora));
                                process_list.get(balanced).addURLs(url);
                                balanced++;
                                if (balanced == HILOS) balanced = 0;
                            } catch (MalformedURLException e) {
                                e.printStackTrace();
                            }
                        }

                    }
                }
            }
    }

    /**
     * Lanza todos los hilos y espera a que se termine de ejecutar
     */
    private static void launch_threads(){
        process_list.forEach(Thread::start);
        process_list.forEach(hilo -> {
            try {
                hilo.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        Process.close_files();
    }
}
