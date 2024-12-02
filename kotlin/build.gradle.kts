plugins {
    kotlin("jvm") version "1.9.20"
}

sourceSets {
    main {
        kotlin.srcDir("src")
    }
}

repositories {
    mavenCentral()
}

tasks {
    wrapper {
        gradleVersion = "8.11"
    }
}