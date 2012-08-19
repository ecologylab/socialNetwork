import socialclient.SocialClient;




public class test{
	
	public static void main(String[] args) { 
		
		
		
		String session = SocialClient.Authenticate("jainit","1234");   // Authenticate with username=jainit and password=1234
	      
        if(session != null){

       SocialClient.GetCurrentUserComp(session);         // Get Information Composition of current logged in user
         
    
       }

}
}