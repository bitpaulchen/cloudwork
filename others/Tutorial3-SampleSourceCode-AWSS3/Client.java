import java.io.*;
import java.net.*;

/**
 *
 * @author darren
 */
public class Client {

    public static void main(String arg[]) throws IOException, ClassNotFoundException {

        int portNum = 11113;

        Socket socket = new Socket("localhost", portNum);

        // Integer Object to send to Server.
        Integer num = 50;

        ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
        ObjectInputStream in = new ObjectInputStream(socket.getInputStream());
        
        out.writeObject(num);
                
        String response = (String) in.readObject();

        System.out.println("Server message: " + response);
        
        //socket.close();
        
    }
}