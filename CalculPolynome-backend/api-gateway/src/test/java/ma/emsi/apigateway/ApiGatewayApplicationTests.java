package ma.emsi.apigateway;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ApplicationContext;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class ApiGatewayApplicationTests {

    @Autowired
    private ApplicationContext applicationContext;

    @Test
    void contextLoads() {
        // Vérifie que le contexte Spring démarre correctement
        assertThat(applicationContext).isNotNull();
    }

    @Test
    void discoveryClientIsEnabled() {
        // Vérifie que le client de découverte (Eureka) est activé
        String[] discoveryBeans = applicationContext.getBeanNamesForAnnotation(org.springframework.cloud.client.discovery.EnableDiscoveryClient.class);
        assertThat(discoveryBeans).isNotEmpty();
    }

    @Test
    void applicationPropertiesLoaded() {
        // Vérifie que les propriétés essentielles sont bien chargées
        String serverPort = applicationContext.getEnvironment().getProperty("server.port");
        assertThat(serverPort).isEqualTo("8081");
    }

    @Test
    void routeConfigurationIsLoaded() {
        // Vérifie que les configurations de routage sont bien chargées dans le contexte
        String gatewayRoutes = applicationContext.getEnvironment().getProperty("spring.cloud.gateway.routes[0].id");
        assertThat(gatewayRoutes).isNotNull();
    }
}
