import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import sun.misc.BASE64Encoder;
import java.net.CookieManager;
import java.util.List;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;


public class InfoShareClient  {
 
     private static final String Boundary = "--7d021a37605f0";
     private static final String get_url = "http://127.0.0.1:8000/i/get_composition/";
     private static final String login_url = "http://127.0.0.1:8000/i/login";
     private static final String post_url = "http://127.0.0.1:8000/i/put_composition/";
      
     public static void main(String[] args) {
    
         String session = Authenticate("jainit","1234");
         if(session != null){
              File infocomp = new File("/home/jainit/Archlinux.png"); 
              PostInfoComposition(session,infocomp);
       //       GetInfoComposition(session,"LTw3QVIezd");
        }
     }
 
    
    public static String Authenticate(String username,String password) {
     
    String cookie = null;

    try {

        URL url = new URL (login_url);
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


    public static int GetInfoComposition(String cookie,String hash_key) {
    
    int response = 0;
    
    try {  

       String info_url = get_url + hash_key + ".meta/";
       URL url = new URL (info_url);         
       HttpURLConnection connection = (HttpURLConnection) url.openConnection();
       connection.setRequestMethod("GET");
       connection.setDoOutput(true);
       connection.setRequestProperty("Cookie", cookie);
       InputStream content = (InputStream)connection.getInputStream();
       BufferedReader in = new BufferedReader (new InputStreamReader (content));
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


    public static String PostInfoComposition(String cookie,File infocomp) {
    try {
         
       URL url = new URL (post_url);
       HttpURLConnection connection = (HttpURLConnection) url.openConnection();
//     connection.setRequestMethod("POST");
       connection.setRequestProperty("Cookie", cookie);
       connection.setDoOutput(true);
       connection.setDoInput(true);
       connection.setUseCaches(false);
       connection.setChunkedStreamingMode(1024);
       connection.getOutputStream().write("name=tropical".getBytes("UTF-8"));
       connection.setRequestProperty("Content-Type", "multipart/form-data; boundary="+ Boundary);
       
       DataOutputStream httpOut = new DataOutputStream(connection.getOutputStream());
          
       File f = infocomp;
       String str = "--" + Boundary + "\r\n"
                   + "Content-Disposition: form-data;name=\"file" + "filename=" + f.getName() + "\"\r\n"
                   + "Content-Type: image/png\r\n"
                   + "\r\n";

       httpOut.write(str.getBytes());

       FileInputStream uploadFileReader = new FileInputStream(f);

       int numBytesToRead = 1024;
       int availableBytesToRead;
       while ((availableBytesToRead = uploadFileReader.available()) > 0)
       {
           byte[] bufferBytesRead;
           bufferBytesRead = availableBytesToRead >= numBytesToRead ? new byte[numBytesToRead]
                            : new byte[availableBytesToRead];
           uploadFileReader.read(bufferBytesRead);
           httpOut.write(bufferBytesRead);
           httpOut.flush();
       }
       httpOut.write(("--" + Boundary + "--\r\n").getBytes());     
       httpOut.write(("--" + Boundary + "--\r\n").getBytes());
       httpOut.flush();
       httpOut.close();

       InputStream is = connection.getInputStream();
       StringBuilder response = new StringBuilder();
       byte[] respBuffer = new byte[4096];
       while (is.read(respBuffer) >= 0)
       {
           response.append(new String(respBuffer).trim());
       }
       is.close();
       System.out.println(response.toString());     
  
   
      }catch(Exception e) {
       e.printStackTrace();
      }
    
     return "1";
    }
        
    

    }
    
