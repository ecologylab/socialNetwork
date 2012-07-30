import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import sun.misc.BASE64Encoder;
import java.net.CookieManager;
import java.util.List;

public class GetInfoComp  {

    public static void main(String[] args) {
    
     String session = Authenticate("jainit","1234");
     System.out.println(session);
     if(session != null){

     PrintUserInfoCompositions(session);

    }

    }

   
    


    public static String Authenticate(String username,String password) {
     
     String cookie = null;
     try {

          URL url = new URL ("http://127.0.0.1:8000/api/info/userlist/");
          String auth_user = username + ":" + password;
          String auth_encoded = new BASE64Encoder().encode(auth_user.getBytes());           
          HttpURLConnection connection = (HttpURLConnection) url.openConnection();
          connection.setRequestMethod("GET");
          connection.setDoOutput(true);
          connection.setRequestProperty("Authorization", "Basic " + auth_encoded);          
          cookie = connection.getHeaderFields().get("Set-Cookie").get(0);
          cookie = cookie.substring(0, cookie.indexOf(";"));    

      } catch(Exception e) {
       e.printStackTrace();
       }
   
      
          return cookie;
    
    }

    public static int PrintUserInfoCompositions(String cookie) {
    
   int response = 0;
    
   try {

            URL url = new URL ("http://127.0.0.1:8000/api/info/userlist/");         
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setDoOutput(true);
            connection.setRequestProperty("Cookie", cookie);

            InputStream content = (InputStream)connection.getInputStream();
            BufferedReader in   = 
                new BufferedReader (new InputStreamReader (content));
            String line;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
	    response = 1;
       } catch(Exception e) {
        e.printStackTrace();
	}
	return response;

    }

    }
    
