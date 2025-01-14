package ma.emsi.eurekaserver;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ApplicationContext;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class EurekaServerApplicationTests {

    @Autowired
    private ApplicationContext applicationContext;

    @Test
    void contextLoads() {
        // Vérifie que le contexte Spring démarre correctement
        assertThat(applicationContext).isNotNull();
    }

    @Test
    void eurekaServerIsRunning() {
        // Vérifie que le serveur Eureka est actif
        String[] eurekaBeans = applicationContext.getBeanNamesForAnnotation(org.springframework.cloud.netflix.eureka.server.EnableEurekaServer.class);
        assertThat(eurekaBeans).isNotEmpty();
    }

    @Test
    void applicationPropertiesLoaded() {
        // Vérifie que certaines propriétés de configuration essentielles sont chargées
        String eurekaServerPort = applicationContext.getEnvironment().getProperty("server.port");
        assertThat(eurekaServerPort).isEqualTo("8761");
    }
}
