// This work is licensed under a Creative Commons Attribution 4.0 International License.
// https://creativecommons.org/licenses/by/4.0/

// Inspiration: https://twitter.com/bigblueboo/status/937341158128197632

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
	vec2 uv = (fragCoord.xy * 2.) / vec2(500) - vec2(1);
    uv *= 5.;	// Scale
    
    // Generate checker pattern
    float c = mod(floor(uv.x) + floor(uv.y), 2.);

    // Color for cross
    vec3 crossc = round(vec3(sin((round(uv.x) - round(uv.y))*2.)*0.5+0.5))*0.4 + 0.5;
    
    // Generate mask for cross
    #define W 0.03
    #define S(a,b) smoothstep(a-W,a+W,b)
    uv = (uv-0.5)*2.;
    float crossm = S(0.95, mod(uv.x, 2.)) * (1.-S(1.05, mod(uv.x, 2.))) * S(0.5, -cos(uv.y * 3.1415)) + 
        S(0.95, mod(uv.y, 2.)) * (1.-S(1.05, mod(uv.y, 2.))) * S(0.5, -cos(uv.x * 3.1415));
    
    
	// Mix between checkerboard and crosses
    fragColor.rgb = mix(vec3(c*0.15 + 0.6), crossc, step(0.1, crossm)*smoothstep(-0.7, 0.4, sin(iTime)));
    
    fragColor.a = 1.;	// Some browsers need the alpha set to 1
}