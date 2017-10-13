import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.Object;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.util.*;
import java.net.Socket;
import java.net.UnknownHostException;
import java.io.FileWriter;

public class PersistentCrawl {
	static PrintWriter out;
	static BufferedReader in;
	static Socket socket;
	// private static String[] outputs;
	static boolean found = false;
	static String csrftoken = "";
	static String sessionid = "";
	static String htmlData = "";
	static int sec_flag_id = 1;

	static class theLock extends Object {
	}

	static ArrayList<String> traversedlinks = new ArrayList<String>();
	static HashSet<String> traversed = new HashSet<String>();

	public static void main(String[] args) {		
		listenSocket();
		login(args[0].toString(),args[1].toString());
	}

	public static void login(String username,String password) {
		String path = "/accounts/login/";
		out.println("GET " + path + " HTTP/1.1");
		out.println("Host: fring.ccs.neu.edu");
		out.println("Connection: Keep-Alive");
		out.println();
		int length = 0;
		int content_length = 0;
		boolean flag_content = false;
		String line = "";
		try {
			File file = new File("sec.txt");
			if (file.exists()) {
				file.delete();
			}
			while ((line = in.readLine()) != null) {
				if (line.contains("Set-Cookie: csrftoken=")) {
					String[] token = line.split("=");
					csrftoken = token[1].split(" ")[0];
					csrftoken = csrftoken.split(";")[0];
				}
				if (line.contains("Set-Cookie: sessionid=")) {
					String[] token = line.split("=");
					sessionid = token[1].split(" ")[0];
					sessionid = sessionid.split(";")[0];
				}
				if (line.contains("Content-Length: ")) {
					length = Integer.parseInt(line.substring("Content-Length: ".length()));
				}
				if (flag_content) {
					content_length += line.length();
					if ((content_length == (length - 6)) || line.endsWith("</html>")) {
						post_request(username,password);
						break;
					}
				}
				if (line.equals("")) {
					flag_content = true;
				}
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void MoveRequest(String path, int depth) {
		out.println("GET " + path + " HTTP/1.1");
		out.println("Host: fring.ccs.neu.edu");
		out.println("Connection: Keep-Alive");
		out.println("Cookie: csrftoken=" + csrftoken + "; sessionid=" + sessionid);
		out.println();
		int length = 0;
		int content_length = 0;
		boolean flag_reopen = false;
		boolean flag_calc = false;
		boolean flag_500 = false;
		boolean flag_302 = false;
		boolean flag_rereq = false;
		String data = "";
		String line = "";
		String Rereq = "";
		try {
			while ((line = in.readLine()) != null) {
				if (line.equals("Connection: close")) {
					flag_reopen = true;
				}
				if (line.contains("Set-Cookie: csrftoken=")) {
					String[] token = line.split("=");
					csrftoken = token[1].split(" ")[0];
					csrftoken = csrftoken.split(";")[0];
				}
				if (line.contains("Set-Cookie: sessionid=")) {
					String[] token = line.split("=");
					sessionid = token[1].split(" ")[0];
					sessionid = sessionid.split(";")[0];
				}
				if (line.contains("Content-Length: ")) {
					length = Integer.parseInt(line.substring("Content-Length: ".length()));
				}
				if (line.contains("500 Internal Server Error")) {
					flag_500 = true;
					Rereq = path;
				}
				if (line.contains("HTTP/1.1 302 FOUND")) {
					flag_302 = true;
				}
				if (line.contains("Location:") && flag_302) {
					Rereq = line.substring(10);
				}
				if (line.equals("")) {
					flag_calc = true;
					if (flag_302 || flag_500) {
						flag_rereq = true;
					}
				}
				if (flag_rereq) {
					if (flag_reopen) {
						listenSocket();
					}
					MoveRequest(Rereq, depth);
					break;

				}
				if (flag_calc) {
					content_length += line.length();
					data += line;
					if (content_length == length || line.endsWith("</html>")) {
						traversed.add(path);
						if (flag_reopen) {
							listenSocket();
							flag_reopen = false;
						}
						parseContent(data, depth);
						break;
					}
				}
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void post_request(String username,String password) {

		String cookie = "csrftoken=" + csrftoken + "; sessionid=" + sessionid;
		String credentials = "username="+username+"&password="+password+"&csrfmiddlewaretoken=" + csrftoken + "&next=";
		out.println("POST /accounts/login/ HTTP/1.1");
		out.println("Host: fring.ccs.neu.edu");
		out.println("Content-Length: 95");
		out.println("Origin: http://fring.ccs.neu.edu");
		out.println("Content-Type: application/x-www-form-urlencoded");
		out.println("Referer: http://fring.ccs.neu.edu/accounts/login/");
		out.println("Cookie: " + cookie);
		out.println("Connection: Keep-Alive");
		out.println();
		out.println(credentials);
		out.println();
		String line = "";
		try {
			while ((line = in.readLine()) != null) {
				if (line.contains("Set-Cookie: csrftoken=")) {
					String[] token = line.split("=");
					csrftoken = token[1].split(" ")[0];
					csrftoken = csrftoken.split(";")[0];
				}
				if (line.contains("Set-Cookie: sessionid=")) {
					String[] token = line.split("=");
					sessionid = token[1].split(" ")[0];
					sessionid = sessionid.split(";")[0];
				}
				if (line.equals("")) {
					MoveRequest("/fakebook/", 0);
					break;
				}
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void parseContent(String htmldata1, int depth) {

		Document doc = Jsoup.parseBodyFragment(htmldata1);
		Element body = doc.body();
		Elements links = body.getElementsByTag("a");
		if (htmldata1.contains("secret_flag")) {
			String sec_flag = htmldata1.split("FLAG:")[1];
			System.out.println("Secret Flag " + sec_flag_id + ": " + sec_flag.split("</h2>")[0]);
			sec_flag_id += 1;
			if (sec_flag_id == 6)
				System.exit(0);
		}
		for (Element link : links) {
			String linkHref = link.attr("href");
			if (!(linkHref.contains("www.ccs.neu.edu") || linkHref.contains("choffnes")
					|| linkHref.contains("northeastern"))) {
				if (!(traversed.contains(linkHref)))
					MoveRequest(linkHref, depth + 1);
			}
		}
	}


	public static void listenSocket() {
		// Create socket connection
		try {
			socket = new Socket("fring.ccs.neu.edu", 80);
			out = new PrintWriter(socket.getOutputStream(), true);
			in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
		} catch (UnknownHostException e) {
			System.out.println("Unknown host");
			System.exit(1);
		} catch (IOException e) {
			System.out.println("No I/O");
			System.exit(1);
		}
	}
}
