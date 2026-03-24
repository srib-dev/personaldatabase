import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.nio.file.Files;
import java.nio.file.Path;
import java.security.KeyFactory;
import java.security.interfaces.ECPrivateKey;
import java.security.interfaces.ECPublicKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

@Configuration

// TODO: Add key rotation
public class KeyConfig {
	@Bean
	public ECPrivateKey jwtPrivateKey() throws Exception {
		String pem = Files.readString(Path.of("/run/secrets/jwt-private-key"));

		String strippedPem = pem.replace("-----BEGIN PRIVATE KEY-----", "")
			.replace("-----END PRIVATE KEY-----", "")
			.replaceAll("\\s", "");

		byte[] KeyBytes = Base64.getDecoder().decode(strippedPem);

		PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(KeyBytes);
		KeyFactory kf = KeyFactory.getInstance("EC");
		return (ECPrivateKey) kf.generatePrivate(spec);

	}
	@Bean
	public ECPublicKey jwtPublicKey() throws Exception {
		String pem = Files.readString(Path.of("/run/secrets/jwt-public-key"));
		String strippedPem = pem.replace("-----BEGIN PUBLIC KEY-----", "")
			.replace("-----END PUBLIC KEY-----", "")
			.replaceAll("\\s", "");
		byte[] KeyBytes = Base64.getDecoder().decode(strippedPem);
		X509EncodedKeySpec spec = new X509EncodedKeySpec(KeyBytes);
		KeyFactory kf = KeyFactory.getInstance("EC");
		return (ECPublicKey) kf.generatePublic(spec);
	}

}
