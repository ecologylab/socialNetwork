package socialclient;
/**
 * 
 * 
 *  Client for Information Composition Social Network  
 * 
 * 
 * 
 */

import java.io.*;
import java.net.*;
import ecologylab.generic.Base64Coder;




public class SocialClient  {
 
     public final static int size=1024;
     private static final String get_url = "http://ecoarray0:3800/i/get_composition/";
     private static final String login_url = "http://ecoarray0:3800/i/login";
     private static final String user_url = "http://ecoarray0:3800/i/list_compositions_by_user/";
 
     public static void main(String[] args) { }
 
    
    public static String Authenticate(String username,String password) {
     
    String cookie = null;

    try {

        URL url = new URL (login_url);
        String auth_user = username + ":" + password;
        String auth_encoded = Base64Coder.encodeString(auth_user);           
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


    public static int GetCurrentUserComp(String cookie) {
    
    int response = 0;
    
    try {  

       String user_list = user_url;
       URL url = new URL (user_list);         
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
    
    
    
    public static int GetUserComp(String cookie,String username) {
    
    int response = 0;
    
    try {  

       String user_list = user_url + username;
       URL url = new URL (user_list);         
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
    
 
    public static void DownloadInfoComp(String fAddress, String destinationDir,String cookie){
    
    int slashIndex =fAddress.lastIndexOf('/');
    int periodIndex =fAddress.lastIndexOf('.');
    
    String fileName=fAddress.substring(slashIndex + 1) + ".icom";

    if (periodIndex >=1 &&  slashIndex >= 0 
    && slashIndex < fAddress.length()-1)
    {
        fileUrl(fAddress,fileName,destinationDir,cookie);
    }
    else
    {
    	fileUrl(fAddress,fileName,destinationDir,cookie);
    }
    }


    private static void fileUrl(String fAddress, String localFileName, String destinationDir,String cookie)  {
    
    OutputStream outStream = null; URLConnection uCon = null;

    InputStream is = null;
    try {
        URL Url;
        byte[] buf;
        int ByteRead,ByteWritten=0;
        Url= new URL(fAddress);
        outStream = new BufferedOutputStream(new
        FileOutputStream(destinationDir+localFileName));
        uCon = Url.openConnection();
        uCon.setRequestProperty("Cookie", cookie);
        is = uCon.getInputStream();
        buf = new byte[size];
        while ((ByteRead = is.read(buf)) != -1) {
            outStream.write(buf, 0, ByteRead);
            ByteWritten += ByteRead;
        }
        System.out.println("Downloaded Successfully.");
        System.out.println("File name:\""+localFileName+ "\"\nNo ofbytes :" + ByteWritten);
    }catch (Exception e) {
        e.printStackTrace();
        }
    finally {
            try {
            is.close();
            outStream.close();
            }
            catch (IOException e) {
        e.printStackTrace();
            }
        }
}
    
        
    public SocialClient(){
    	
    }   
                 
}


    
