package es.dmmop;

import com.jayway.jsonpath.JsonPath;
import com.jayway.jsonpath.PathNotFoundException;
import net.minidev.json.JSONObject;

import java.util.HashMap;

public class Extractor {
    private static final String EVENT_TYPE1 = "PullRequestReviewCommentEvent";
    private static final String EVENT_TYPE2 = "PullRequestEvent";
    private static final String EVENT_TYPE3 = "PushEvent";

    private static final String ID_EXPR = "$.repo.id";
    private static final String HEAD_EXPR = "$.payload.pull_request.head.repo.language";
    private static final String BASE_EXPR = "$.payload.pull_request.base.repo.language";
    private static final String TYPE_EXPR = "$.type";
    private static final String TIME_EXPR = "$.created_at";
    private static final String SIZE_EXPR = "$.payload.size";

    public static final int LANG_TYPE = 0;
    public static final int COMMIT_TYPE = 1;

    /**
     * Recibe la línea del json completo y decide que acción realizar con ella.
     *
     * @param line Json completo del evento
     * @return String con los datos extraidos del json
     */
    public String[] extract(String line) throws PathNotFoundException {
        line = line.replaceAll("\n", ""); // Normalizar línea
        String result[] = new String[2];
        int type = check_type(line); //Comprobar type event

        if (type == LANG_TYPE) {
            result[0] = extract_langs(line);
            result[1] = String.valueOf(LANG_TYPE);
        } else if (type == COMMIT_TYPE) {
            result[0] = extract_commits(line);
            result[1] = String.valueOf(COMMIT_TYPE);

        } else result = null;

        return result;
    }

    /**
     * Evalua de qué tipo es el evento, 0 si se puede extraer el lenguage,
     * 1 si se un commit ó -1 si no tiene valor.
     *
     * @param line Recibe el Json completo
     * @return Integer
     */
    private int check_type(String line) throws PathNotFoundException {
        int type_num = -1;
        String type = JsonPath.read(line, TYPE_EXPR);

        if (type.equalsIgnoreCase(EVENT_TYPE1) || type.equalsIgnoreCase(EVENT_TYPE2)) type_num = LANG_TYPE;
        else if (type.equalsIgnoreCase(EVENT_TYPE3)) type_num = COMMIT_TYPE;
        else type_num = -1;

        return type_num;
    }

    /**
     * Extrae la Id del repositorio, su cabecera y su base.
     *
     * @param line Recibe el Json completo
     * @return String con los datos sobre lenguage extraidos del json
     */
    private String extract_langs(String line) throws PathNotFoundException {
        HashMap<String, String> language_event = new HashMap<>();
        language_event.put("id", JsonPath.read(line, ID_EXPR).toString());
        language_event.put("repo_head_lang", JsonPath.read(line, HEAD_EXPR));
        language_event.put("repo_base_lang", JsonPath.read(line, BASE_EXPR));

        return new JSONObject(language_event).toJSONString();
    }

    /**
     * Extrae la Id del repositorio, su el tamaño y la fecha de creación.
     *
     * @param line Recibe el Json completo
     * @return String con los datos sobre lenguage extraidos del json
     */
    private String extract_commits(String line) throws PathNotFoundException {
        HashMap<String, String> language_event = new HashMap<>();
        language_event.put("id", JsonPath.read(line, ID_EXPR).toString());
        language_event.put("size", JsonPath.read(line, SIZE_EXPR).toString());
        language_event.put("time", JsonPath.read(line, TIME_EXPR).toString().substring(0, 10));

        return new JSONObject(language_event).toJSONString();
    }
}
