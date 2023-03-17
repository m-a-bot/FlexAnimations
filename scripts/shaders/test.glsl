
void mainImage(out vec4 fragColor, in vec2 fragCoord) {

    vec2 uv = fragCoord / iResolution.xy;

    vec2 rpos = uv - 0.5;

    rpos.y /= iResolution.x / iResolution.y;

    float distance = length(rpos);

    if (distance > 0.35) {

        fragColor = vec4(0, 0.5, 0.8, 1);

    }

    else if (distance > 0.1) {

        fragColor = vec4(1, 0.4, 0.1, 0.6);

    }

    else {
        fragColor = vec4(1,1,1,1);
    }
}