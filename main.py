import math
app.stepsPerSecond = 20;

### class infrastructure
class LinAlg:
    
    # returns rotation matrix around axis given theta
    def return_mat_rx(a):
        return Mat4x4([
            [1, 0,           0,            0],
            [0, math.cos(a), -math.sin(a), 0],
            [0, math.sin(a),  math.cos(a), 0],
            [0, 0,           0,            1]
        ]);
    def return_mat_ry(a):
        return Mat4x4([
            [math.cos(a),    0,    -math.sin(a),    0],
            [0          ,    1,    0           ,    0],
            [math.sin(a),    0,    math.cos(a) ,    0],
            [0          ,    0,    0           ,    1]
        ]);
    def return_mat_rz(a):
        return Mat4x4([
            [math.cos(a), -math.sin(a), 0, 0],
            [math.sin(a),  math.cos(a), 0, 0],
            [0,            0,           1, 0],
            [0,            0,           0, 1]
        ]);
    # returns translation or scaling matrix given values
    def return_mat_trans(x, y, z):
        return Mat4x4([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ]);
    def return_mat_scale(x, y, z):
        return Mat4x4([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ]);
    
    # multiplies vector with matrix
    def mat_mult(vec, mat):
    
        v = V3(
            vec.x * mat[0][0] + vec.y * mat[0][1] + vec.z * mat[0][2] + mat[0][3],
            vec.x * mat[1][0] + vec.y * mat[1][1] + vec.z * mat[1][2] + mat[1][3],
            vec.x * mat[2][0] + vec.y * mat[2][1] + vec.z * mat[2][2] + mat[2][3]
        );
        v.w = vec.x * mat[3][0] + vec.y * mat[3][1] + vec.z * mat[3][2] + mat[3][3];
        
        return v;
    
    def dot_prod(v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
    def cross_prod(v1, v2):
        return V3(
            v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x
        );
    
    def normalize(v):
        d = distance(0, 0, distance(0, 0, v.x, v.z), v.y);
        return V3(v.x / d, v.y / d, v.z / d);
    
    # inverts camera projection matrix
    def mat_quick_inverse(matrix):
        m = matrix.m;
        trans = V3(m[0][3], m[1][3], m[2][3]);
        return Mat4x4([
            [m[0][0],     m[1][0],     m[2][0],     LinAlg.dot_prod(-1 * trans, V3(m[0][0], m[1][0], m[2][0]))],
            [m[0][1],     m[1][1],     m[2][1],     LinAlg.dot_prod(-1 * trans, V3(m[0][1], m[1][1], m[2][1]))],
            [m[0][2],     m[1][2],     m[2][2],     LinAlg.dot_prod(-1 * trans, V3(m[0][2], m[1][2], m[2][2]))],
            [0      ,     0      ,     0      ,     1                                                  ]
        ]);
    
    
    
        ### for clipping purposes
    
    # clipping functions; useless now bc too laggy
    def line_plane_intersect(plane_p, plane_n, line_start, line_end):
        n = LinAlg.normalize(plane_n);
        line_dir = line_end - line_start;
        
        numer = LinAlg.dot_prod(plane_p - line_start, n);
        denom = LinAlg.dot_prod(line_dir, n);
        
        if(denom == 0):
            raise Exception("error in line_plane_intersect; the line given is parellel to the plane given");
        
        val = numer / denom;
        
        return line_start + val * line_dir;
    def clip_against_plane(plane_p, plane_n, input_tri):
        
        plane_n = LinAlg.normalize(plane_n);
        
        def dist(p):
            return LinAlg.dot_prod(p - plane_p, plane_n);
        
        inside_points = [];
        outside_points = [];
        
        d0 = dist(input_tri.p[0]);
        d1 = dist(input_tri.p[1]);
        d2 = dist(input_tri.p[2]);
        
        if(d0 >= 0):
            inside_points.append(input_tri.p[0]);
        else:
            outside_points.append(input_tri.p[0]);
        
        if(d1 >= 0):
            inside_points.append(input_tri.p[1]);
        else:
            outside_points.append(input_tri.p[1]);
            
        if(d2 >= 0):
            inside_points.append(input_tri.p[2]);
        else:
            outside_points.append(input_tri.p[2]);
            
        
        if(len(inside_points) == 0):
            return [];
        if(len(inside_points) == 3):
            return [input_tri];
        
        if(len(inside_points) == 1 and len(outside_points) == 2):
            output_tri1 = Triangle([
                inside_points[0],
                LinAlg.line_plane_intersect(plane_p, plane_n, inside_points[0], outside_points[0]),
                LinAlg.line_plane_intersect(plane_p, plane_n, inside_points[0], outside_points[1])
            ]);
            
            return [output_tri1];
        
        if(len(inside_points) == 2 and len(outside_points) == 1):
            output_tri1 = Triangle([
                inside_points[0],
                LinAlg.line_plane_intersect(plane_p, plane_n, inside_points[0], outside_points[0]),
                LinAlg.line_plane_intersect(plane_p, plane_n, inside_points[1], outside_points[0])
            ]);
            
            output_tri2 = Triangle([
                inside_points[1],
                inside_points[0],
                output_tri1.p[2]
            ]);
            
            
            return [output_tri1, output_tri2];
        
        raise Exception("something went horribly wrong in your clipping function")

    # checking trapezoidal boundaries
    def within_trapezoid(self, trap, p):
        for face in trap.faces:
            # need to get inside-pointing normal
            line1 = face.p[1] - face.p[0];
            line2 = face.p[2] - face.p[1];
            normal = LinAlg.normalize(LinAlg.cross_prod(line1, line2));
            if(LinAlg.dot_prod(normal, p-normal) < 0):
                return False;
        return True;

class Color:
    def __init__(self, r=0, g=0, b=0, a=100):
        self.r, self.g, self.b, self.a = r, g, b, a;
    
    def return_rgb(self):
        return rgb(math.floor(self.r), math.floor(self.g), math.floor(self.b));
    def return_a(self):
        return self.a;
    
    def __mul__(self, n):
        return Color(self.r * n, self.g * n, self.b * n);
    def __imul__(self, n):
        self.r *= n; self.g *= n; self.b *= n;
        return self;
    
    def __str__(self):
        return f"r: {self.r}, g: {self.g}, b: {self.b}";

# vectors
class V2:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y;
    def tuple(self):
        return self.x, self.y;
        
    def __add__(self, v):
        return V2(self.x+v.x, self.y+v.y);
    def __iadd_(self, v):
        self.x += v.x; self.y += v.y; 
        return self;
    
    def __sub__(self, v):
        return V2(self.x-v.x, self.y-v.y);
    def __rsub__(self, v):
        return V2(v.x-self.x, v.y-self.y);
    
    def __mul__(self, n):
        return V2(self.x*n, self.y*n);
    def __rmul__(self, n):
        return V2(self.x*n, self.y*n);
    def __imul__(self, n):
        self.x *= n; self.y *= n;
        return self;
    
    def __truediv__(self, n):
        return V2(self.x/n, self.y/n);
    def __itruediv__(self, n):
        self.x /= n; self.y /= n;
        return self;
    def __rtruediv__(self, n):
        raise Exception("why are you dividing a scalar by a vector");    
    
    def __str__(self):
        return f"2d vector, x: {self.x}, y: {self.y}";

class V3:
    def to_points(coords):
        p = [];
        for i in range(len(coords)):
            if(i % 3 == 0):
                p.append(V3(coords[i], coords[i+1], coords[i+2]));
        return p;
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z;
    
    def list(self):
        return [self.x, self.y, self.z];
    
    def __str__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}";
    
    def __add__(self, v):
        return V3(self.x+v.x, self.y+v.y, self.z+v.z);
    def __iadd_(self, v):
        self.x += v.x; self.y += v.y; self.z += v.z;
        return self;
    
    def __sub__(self, v):
        return V3(self.x-v.x, self.y-v.y, self.z-v.z);
    def __rsub__(self, v):
        return V3(v.x-self.x, v.y-self.y, v.z-self.z);
    
    def __mul__(self, n):
        return V3(self.x*n, self.y*n, self.z*n);
    def __rmul__(self, n):
        return V3(self.x*n, self.y*n, self.z*n);
    def __imul__(self, n):
        self.x *= n; self.y *= n; self.z *= n;
        return self;
    
    def __truediv__(self, n):
        return V3(self.x/n, self.y/n, self.z/n);
    def __itruediv__(self, n):
        self.x /= n; self.y /= n; self.z /= n;
        return self;
    def __rtruediv__(self, n):
        raise Exception("why are you dividing a scalar by a vector");


# shapes
class Triangle:
    def to_tris(points):
        p = [];
        for i in range(len(points)):
            if(not i % 3):
                p.append(Triangle([points[i], points[i+1], points[i+2]]));
        return p;
    
    def __init__(self, p=V3.to_points([0, 0, 0,     0, 0, 0,     0, 0, 0]), color=Color(0, 0, 0)):
        self.p = p
        self.color = color;
    
    def __str__(self):
        return f"color: {self.color}, p1: {self.p[0]}, p2: {self.p[1]}, p3: {self.p[2]}";
class Mesh:
    def create_rect(cx, cy, cz, sx=1, sy=1, sz=1):
        rect = Mesh(Triangle.to_tris(V3.to_points([
            # south face
            0, 0, 0,    0, 1, 0,     1, 1, 0,    
            0, 0, 0,    1, 1, 0,     1, 0, 0,
            # east face
            1, 0, 0,    1, 1, 0,     1, 1, 1, 
            1, 0, 0,    1, 1, 1,     1, 0, 1,
            # north face
            1, 0, 1,    1, 1, 1,     0, 1, 1, 
            1, 0, 1,    0, 1, 1,     0, 0, 1,
            # west face
            0, 0, 1,    0, 1, 1,    0, 1, 0,
            0, 0, 1,    0, 1, 0,    0, 0, 0,
            # top face
            0, 1, 0,    0, 1, 1,    1, 1, 1,
            0, 1, 0,    1, 1, 1,    1, 1, 0,
            # bottom face
            0, 0, 0,    1, 0, 0,    1, 0, 1,
            0, 0, 0,    1, 0, 1,    0, 0, 1
        ])));
        rect.translate(cx, cy, cz);
        rect.scale(sx, sy, sz);
        return rect;
        
    def __init__(self, tris):
        self.tri = tris;
        
    def translate(self, x, y, z):
        new_tris = [];
        mat_trans = LinAlg.return_mat_trans(x, y, z);
        for tri in self.tri:
            new_tri = Triangle([
                LinAlg.mat_mult(tri.p[0], mat_trans.m),
                LinAlg.mat_mult(tri.p[1], mat_trans.m),
                LinAlg.mat_mult(tri.p[2], mat_trans.m)
            ]);
            new_tris.append(new_tri);
        self.tri = new_tris;
        
    def scale(self, x, y, z):
        new_tris = [];
        mat_scale = LinAlg.return_mat_scale(x, y, z);
        for tri in self.tri:
            new_tri = Triangle([
                LinAlg.mat_mult(tri.p[0], mat_scale.m),
                LinAlg.mat_mult(tri.p[1], mat_scale.m),
                LinAlg.mat_mult(tri.p[2], mat_scale.m)
            ]);
            new_tris.append(new_tri);
        self.tri = new_tris;
    
    def __str__(self):
        return f"mesh, tri len: {len(self.tri)}, tri: {self.tri}"
class Rect_Prism:
    def __init__(self, cx, cy, cz, sx, sy, sz, color, opacity, theta=0):
        self.mesh = Mesh.create_rect(cx, cy, cz, sx, sy, sz);
        for tri in self.mesh.tri:
            tri.color = color;
            tri.color.a = opacity;
        self.theta = theta;

class Rotation:
    def __init__(self, axis, dir, layer):
        self.axis = axis;
        self.dir = dir;
        self.layer = layer;
    def data(self):
        return self.axis, self.dir, self.layer;
class Cubie:
    face_codes = {
        'north': 2,
        'east': 3,
        'south': 0,
        'west': 1,
        'top': 5,
        'bottom': 4
    };
    color_codes = {
        'south': Color(0, 255, 0), # green
        'east': Color(255, 0, 0), # red
        'north': Color(0, 0, 255), # blue
        'west': Color(253, 170, 19), # orange
        'top': Color(255, 255, 255), # white
        'bottom': Color(255, 255, 0) # yellow
    };
    
    def __init__(self, cx, cy, cz):
        self.mesh = Mesh.create_rect(cx, cy, cz);
        self.theta = 0;
    
    def color(self, face, color):
        self.mesh.tri[Cubie.face_codes[face] * 2].color = color;
        self.mesh.tri[Cubie.face_codes[face] * 2 + 1].color = color;
    
    def __str__(self):
        return f"x+: {self.mesh.tri[2].color}, \nx-: {self.mesh.tri[6].color}, \nz-: {self.mesh.tri[0].color}, \nz-\+: {self.mesh.tri[4].color}, \ny+: {self.mesh.tri[8].color}, \ny-: {self.mesh.tri[10].color}";
class Rubix:
    def create_rubix(n):
    
        rubix = [];
        
        for i in range(n):
            
            layer = [];
            
            for j in range(n):
                
                row = [];
                
                for k in range(n):
                    
                    cubie = Cubie(j-n/2, i-n/2, k-n/2);
                    
                    # coloring cubie
                    if(i == n-1):
                        cubie.color('bottom', Cubie.color_codes['bottom']);
                    elif(i == 0):
                        cubie.color('top', Cubie.color_codes['top']);
                    
                    if(j == n-1):
                        cubie.color('west', Cubie.color_codes['west']);
                    elif(j == 0):
                        cubie.color('east', Cubie.color_codes['east']);
                    
                    if(k == 0):
                        cubie.color('south', Cubie.color_codes['south']);
                    elif(k == n-1):
                        cubie.color('north', Cubie.color_codes['north']);
                    
                    row.append(cubie);
                
                layer.append(row);  
            
            rubix.append(layer);
        
        return Rubix(rubix);
    
    axis_to_rot_mat = {
        'x': LinAlg.return_mat_rx,
        'y': LinAlg.return_mat_ry,
        'z': LinAlg.return_mat_rz
    };
    

    def __init__(self, cubes):
        self.cubies = cubes;
        self.solved_cubies = cubes.copy();
        self.cubies_to_update = [];
        
        self.rotate_cue = [];
        self.rotate_axis = '';
        self.rotate_speed = math.pi*2 / app.stepsPerSecond;
        # properties can be used for any axis of rotation, so long as two rotation actions do not occur at once
        self.theta = 0;
        self.rotate_dir = 0;
        self.rotate_layer = 'invalid';
        
    
    
    def cubie_list(self):
        l = [];
        for layer in self.cubies:
            for row in layer:
                for cubie in row:
                    l.append(cubie);
        return l;
    def cubies_at_pos(self, axis, layer):
        if(axis == 'x'):
            return [self.cubies[0][layer][0], self.cubies[0][layer][1], self.cubies[1][layer][1], self.cubies[1][layer][0]];
        if(axis == 'y'):
            return [self.cubies[layer][0][0], self.cubies[layer][0][1], self.cubies[layer][1][1], self.cubies[layer][1][0]];
        if(axis == 'z'):
            return [self.cubies[0][0][layer], self.cubies[0][1][layer], self.cubies[1][1][layer], self.cubies[1][0][layer]];
    # integrates in clockwise direction
    def integrate_cubies(self, cubies):
        if(self.rotate_axis == 'x'):
            self.cubies[0][self.rotate_layer][0] = cubies[0];
            self.cubies[0][self.rotate_layer][1] = cubies[1]
            self.cubies[1][self.rotate_layer][1] = cubies[2];
            self.cubies[1][self.rotate_layer][0] = cubies[3]; 
        elif(self.rotate_axis == 'y'):
            self.cubies[self.rotate_layer][0][0] = cubies[0];
            self.cubies[self.rotate_layer][0][1] = cubies[1];
            self.cubies[self.rotate_layer][1][1] = cubies[2];
            self.cubies[self.rotate_layer][1][0] = cubies[3];
        elif(self.rotate_axis == 'z'):
            self.cubies[0][0][self.rotate_layer] = cubies[0];
            self.cubies[0][1][self.rotate_layer] = cubies[1];
            self.cubies[1][1][self.rotate_layer] = cubies[2];
            self.cubies[1][0][self.rotate_layer] = cubies[3];
    
    def cue_rotate(self, axis, dir, layer):
        self.rotate_cue.append(Rotation(axis, dir, layer));
        if(len(self.rotate_cue) == 1):
            self.execute_rotate();
        
    def execute_rotate(self):
        rotation = self.rotate_cue[0];
        self.define_rotate(rotation.axis, rotation.dir, rotation.layer); 
    
    def define_rotate(self, axis, dir, layer):
        if(self.rotate_axis):
            return;
        
        self.rotate_axis = axis;
        self.rotate_dir = dir;
        self.rotate_layer = layer;
        
        self.cubies_to_update = self.cubies_at_pos(axis, layer);
        # updating cubies list for rotation
        rotated_cubies = self.cubies_to_update.copy();
        
        
        if((dir > 0 and axis == 'z') or (dir < 0 and axis != 'z')):
            rotated_cubies.insert(0, rotated_cubies.pop(len(rotated_cubies)-1));
        elif((dir > 0 and axis != 'z') or (dir < 0 and axis == 'z')):
            rotated_cubies.append(rotated_cubies.pop(0));
        
        self.integrate_cubies(rotated_cubies);
    
    def finish_rotate(self):
        self.cubies_to_update = [];
        self.theta = 0;
        self.rotate_dir = 0;
        self.rotate_layer = 'invalid';
        self.rotate_axis = '';
        if(len(self.rotate_cue)):
            self.rotate_cue.pop(0);
        if(len(self.rotate_cue)):
            self.execute_rotate();
    
    def update_rotate(self):
        
        self.theta += self.rotate_speed * self.rotate_dir;
        if(abs(self.theta) >= math.pi/2):
            # mutating points
            mut_mat = Rubix.axis_to_rot_mat[self.rotate_axis](math.pi/2 * self.rotate_dir);
            for cubie in self.cubies_to_update:
                cubie.theta = 0;
                for tri in cubie.mesh.tri:
                    for i in range(len(tri.p)):
                        tri.p[i] = LinAlg.mat_mult(tri.p[i], mut_mat.m);
            
            self.finish_rotate();
            return True;
        
        for cubie in self.cubies_to_update:
            cubie.theta = self.theta;
        
        return False;

    def solve(self):
        self.cubies = self.solved_cubies;
    def shuffle(self):
        temp = self.rotate_speed;
        self.rotate_speed = math.pi/2;
        
        i = 0;
        move_len = randrange(25, 35);
        all_axis = ['x', 'y', 'z']
        while(i < move_len):
            axis = all_axis[randrange(0, 3)];
            dir = randrange(0, 2) * 2 - 1;
            layer = randrange(0, 2);
            self.cue_rotate(axis, dir, layer);
            i += 1;
        
        while(len(self.rotate_cue)):
            self.update_rotate();
        
        self.rotate_speed = temp;
        
    
    def update(self):
        if(self.rotate_axis):
            self.update_rotate();

# matrix struct
class Mat4x4:
    def __init__(self, mat=None):
        self.m = mat;

class Camera:
    
    def return_mat_proj(aspect_ratio, FOV_scale, q, z_near):
        return Mat4x4([
            [aspect_ratio * FOV_scale,   0        ,   0,   0          ],
            [0                       ,   FOV_scale,   0,   0          ],
            [0                       ,   0        ,   q,   -z_near * q],
            [0                       ,   0        ,   1,   1          ]
        ]);
    
    def point_at(pos, target, up):
        forw = LinAlg.normalize(target - pos);
        up = LinAlg.normalize(up - LinAlg.dot_prod(forw, up) * forw);
        right = LinAlg.cross_prod(forw, up);
        return Mat4x4([
            [right.x,     up.x,     forw.x,     pos.x],
            [right.y,     up.y,     forw.y,     pos.y],
            [right.z,     up.z,     forw.z,     pos.z],
            [0      ,     0   ,     0     ,     1    ]
        ]);
    
    def scale_to_screen(v):
        return V3((v.x + 1) / 2 * Camera.W, (v.y + 1) / 2 * Camera.H, v.z);
    
    def draw_tri(tri, col, wire_frame):
        fill_col = col.return_rgb();
        line_col = 'black';
        if(not wire_frame):
            line_col = fill_col;
        opacity = col.return_a();
        Polygon(tri[0].x, 400-tri[0].y, tri[1].x, 400-tri[1].y, tri[2].x, 400-tri[2].y, fill=fill_col, opacity=opacity, border=line_col, borderWidth=1.2);
    def draw_face(face, col):
        Polygon(face[0].x, face[0].y, face[1].x, face[1].y, face[2].x, face[2].y, face[3].x, face[3].y, fill=col, border='black');
    
    # projection properties
    W, H = 400, 400;
    aspect_ratio = H / W;
    FOV = math.pi/2 -1
    FOV_scale = 1 / math.tan(FOV/2);
    
    # z far is farthest distance point can be to still be visible
    # z near is closest distance point can be to still be visible; otherwise is clipped
    z_far = 1000; z_near = 0.1; q = z_far / (z_far - z_near);
    mat_proj = return_mat_proj(aspect_ratio, FOV_scale, q, z_near);
    
    
    def __init__(self, x=0, y=0, z=0, dx=0, dy=0, dz=1):
        self.pos = V3(x, y, z); self.setup_pos = V3(*self.pos.list());
        self.init_dir = LinAlg.normalize(V3(dx, dy, dz)); self.setup_dir = V3(*self.init_dir.list());
        self.dir = self.init_dir;
        self.up = V3(0, 1, 0);
        
        self.yaw = 0;
        self.pitch = 0;
        
        self.translate_speed = 7 / app.stepsPerSecond;
        self.rotate_speed = 0.9 / app.stepsPerSecond;
    
    def orbit_origin(self, v):
        ry = LinAlg.return_mat_ry(v.x / 800 * math.pi);
        self.pos = LinAlg.mat_mult(self.pos, ry.m);
        self.init_dir = LinAlg.mat_mult(self.dir, ry.m);
    def toggle_y(self):
        self.pos.y = -1 * self.pos.y;
        self.init_dir.y = -1 * self.init_dir.y;
    
    def __str__(self):
        return f"camera";


class Mouse:
    prev_pos = V2();
    cur_pos = V2();
    init_down_pos = V2();
    init_up_pos = V2();
    down = False;
    move_time = 0;
    down_time = 0;
    up_time = 0;
    
    def set_pos(x, y):
        Mouse.cur_pos = V2(x, y);
    def set_init_down(x, y):
        Mouse.down = True;
        Mouse.up_time = 0;
        Mouse.init_down_pos = V2(x, y);
    def set_init_up(x, y):
        Mouse.down = False;
        Mouse.down_time = 0;
        Mouse.init_up_pos = V2(x, y);
    def pos():
        return [Mouse.cur_pos.x, Mouse.cur_pos.y];
class Key:
    def __init__(self, char):
        self.char = char;
        self.down_time = 0;
    def __str__(self):
        return f"char: {self.char}, down_time: {self.down_time}"
class Keyboard:
    keys = [];
    
    def contains(char):
        for key in Keyboard.keys:
            if(key.char == char):
                return True;
        return False;
    
    def update_keys():
        for key in Keyboard.keys:
            key.down_time += 1;

### main class
class Program:
    
    # 0 denotes home, 1 denotes info, 2 denotes game
    screen_i = 0;
    
    # general properties
    debug = False;
    #mouse_movement = True;
    
    # camera properties
    camera = Camera(-4, 4, -4, 4, -4, 4);
    # lighting properties
    light_dir = LinAlg.normalize(V3(0, 1, -1));
    min_lighting_val = 0.2;
    
    rubix = Rubix.create_rubix(2);
    x_axis = Rect_Prism(0.33, 0, 0, 3, 0.1, 0.1, Color(255, 30, 30), 50);
    y_axis = Rect_Prism(0, 0.33, 0, 0.1, 3, 0.1, Color(30, 255, 30), 50);
    z_axis = Rect_Prism(0, 0, 0.33, 0.1, 0.1, 3, Color(30, 30, 255), 50);
    game_objs = [*rubix.cubie_list(), x_axis, y_axis, z_axis];
    
    
    button_pressed = False;
    
    # determines 2d screen points from 3d objects
    def render(objs):
        # setting up camera info
        mat_camera_rot_y = LinAlg.return_mat_ry(Program.camera.yaw);
        mat_camera_rot_x = LinAlg.return_mat_rx(Program.camera.pitch);
        
        Program.camera.dir = LinAlg.normalize(LinAlg.mat_mult(LinAlg.mat_mult(Program.camera.init_dir, mat_camera_rot_x.m), mat_camera_rot_y.m));
        target = Program.camera.pos + Program.camera.dir;
        # when multiplied with 3d point, projects into 'camera space'
        mat_camera = Camera.point_at(Program.camera.pos, target, Program.camera.up);
        # reverses camera rotation and translation and projects points based on this reverse
        mat_view = LinAlg.mat_quick_inverse(mat_camera);
        
        tris_to_raster = [];
        
        # converting 3d point into 2d point
        for obj in objs:
            for tri in obj.mesh.tri:
                tri_rot, tri_view, tri_proj, tri_scaled = Triangle(), Triangle(), Triangle(), Triangle();
                
                # rotates triangle is undergoing current rubix rotation
                if(obj.theta):
                    rot_mat = Rubix.axis_to_rot_mat[Program.rubix.rotate_axis](obj.theta);
                    tri_rot.p[0] = LinAlg.mat_mult(tri.p[0], rot_mat.m);
                    tri_rot.p[1] = LinAlg.mat_mult(tri.p[1], rot_mat.m);
                    tri_rot.p[2] = LinAlg.mat_mult(tri.p[2], rot_mat.m);
                else:
                    tri_rot = tri;
                    
                # creating normal of triangle
                line1 = tri_rot.p[1] - tri_rot.p[0];
                line2 = tri_rot.p[2] - tri_rot.p[1];
                normal = LinAlg.normalize(LinAlg.cross_prod(line1, line2));
                
                # testing if triangle is visible; only then would want to perform more calculations
                if(LinAlg.dot_prod(normal, tri_rot.p[1] - Program.camera.pos) < 0.1):
                
                    # converting to camera view (world space -> view space)
                    tri_view.p[0] = LinAlg.mat_mult(tri_rot.p[0], mat_view.m);
                    tri_view.p[1] = LinAlg.mat_mult(tri_rot.p[1], mat_view.m);
                    tri_view.p[2] = LinAlg.mat_mult(tri_rot.p[2], mat_view.m);
                    
                    # clipping triangles if too close to screen
                    plane_p = V3(0, 0, 1);
                    plane_n = V3(0, 0, 1);
                    #tris_clipped = LinAlg.clip_against_plane(plane_p, plane_n, tri_view);
                    tris_clipped = [tri_view];
                    
                    for tri_clipped in tris_clipped:
                    
                        # projecting on screen (multiplying point with projection matrix)
                        tri_proj.p[0] = LinAlg.mat_mult(tri_clipped.p[0], Camera.mat_proj.m); tri_proj.p[0] /= tri_proj.p[0].w;
                        tri_proj.p[1] = LinAlg.mat_mult(tri_clipped.p[1], Camera.mat_proj.m); tri_proj.p[1] /= tri_proj.p[1].w;
                        tri_proj.p[2] = LinAlg.mat_mult(tri_clipped.p[2], Camera.mat_proj.m); tri_proj.p[2] /= tri_proj.p[2].w;
                        
                        # point scaling to screen
                        tri_scaled.p[0] = Camera.scale_to_screen(tri_proj.p[0]);
                        tri_scaled.p[1] = Camera.scale_to_screen(tri_proj.p[1]);
                        tri_scaled.p[2] = Camera.scale_to_screen(tri_proj.p[2]);
                        
                        # really janky lighting effect
                        val = (LinAlg.dot_prod(normal, Program.light_dir) + 1) / 2 * (1-Program.min_lighting_val) + Program.min_lighting_val;
                        tri_col = tri.color * val; tri_col.a = tri.color.a;
                        
                        # storing triangle to be sorted and drawn
                        tris_to_raster.append(Triangle([tri_scaled.p[0], tri_scaled.p[1], tri_scaled.p[2]], tri_col));
        
        # makes sure there are objects to draw
        if(not len(tris_to_raster)):
            return;
        
        # sorts order to draw triangles by z distance (closest triangle = last to be drawn)
        sorted_tris_to_raster = [tris_to_raster[0]];
        for i in range(1, len(tris_to_raster)):
            
            cur_z = (tris_to_raster[i].p[0].z + tris_to_raster[i].p[1].z + tris_to_raster[i].p[2].z) / 3;
            
            j = 0;
            appended = False;
            while(j < len(sorted_tris_to_raster) and not appended):
                
                sorted_z = (sorted_tris_to_raster[j].p[0].z + sorted_tris_to_raster[j].p[1].z + sorted_tris_to_raster[j].p[2].z) / 3;
                
                if(cur_z > sorted_z):
                    sorted_tris_to_raster.insert(j, tris_to_raster[i]);
                    appended = True;
                j += 1;
            if(not appended):
                sorted_tris_to_raster.append(tris_to_raster[i]);
        
        
        # drawing triangles
        for sorted_tri in sorted_tris_to_raster:
            
            cue = [sorted_tri];
            
            # disabled clipping bc too laggy
            """
            tris_to_add = 1;
            for i in range(4):
                tris_to_add = len(cue);
                while(tris_to_add > 0):
                    tri = cue.pop(0);
                    tris_to_add -= 1;
                    
                    clipped = [];
                    if(i == 0):
                        clipped = LinAlg.clip_against_plane(V3(0, 0, 0), V3(1, 0, 0), tri);
                    elif(i == 1):
                        clipped = LinAlg.clip_against_plane(V3(0, 0, 0), V3(0, 1, 0), tri);
                    elif(i == 2):
                        clipped = LinAlg.clip_against_plane(V3(Program.camera.W-1, 0, 0), V3(-1, 0, 0), tri);
                    elif(i == 3):
                        clipped = LinAlg.clip_against_plane(V3(0, Program.camera.H-1, 0), V3(0, -1, 0), tri);
                    
                    for clipped_tri in clipped:
                        cue.append(clipped_tri);
            """
            
            # drawing triangles
            for tri in cue:
                Camera.draw_tri(tri.p, sorted_tri.color, Program.debug);
        
        # drawing circles at vertices
        if(Program.debug):
            for tri in sorted_tris_to_raster:
                
                Circle(tri.p[0].x, tri.p[0].y, 5, fill='orange');
                Circle(tri.p[1].x, tri.p[1].y, 5, fill='orange');
                Circle(tri.p[2].x, tri.p[2].y, 5, fill='orange');
    
    def update_home():
        screen = Group(
            Rect(0, 0, 400, 400, fill='white'),
            Label("3D RENDERED RUBIX CUBE", 200, 100, size=25),
            Group(
                Rect(90, 345, 60, 30, fill='lightGrey'),
                Label('Try', 120, 360),
            ),
            Group(
                Rect(250, 345, 60, 30, fill='lightGrey'),
                Label('Info', 280, 360)
            )
        );
        
        if(Mouse.down and screen.children[2].hits(*Mouse.pos())):
            Program.screen_i = 2;
            screen.visible = False;
        elif(Mouse.down and screen.children[3].hits(*Mouse.pos())):
            Program.screen_i = 1;
            screen.visible = False;
    
    def update_info():
        screen = Group(
            Rect(0, 0, 400, 400, fill='white'),
            Group(
                Rect(20, 345, 60, 30, fill='lightGrey'),
                Label('Home', 50, 360),
            ),
            Group(
                Label('Info', 200, 50, size=20),
                Label('Pressing a, s, and d will rotate the cube clockwise along the', 200, 90),
                Label('x, y, and z axis on the layer touching the axis of rotation', 200, 120),
                Label('Pressing the capitalized letters (A, S, D) rotate the layer', 200, 150),
                Label('counter-clockwise', 200, 180),
                Label('Pressing i (or I) simultaneously when you press the letters will', 200, 210),
                Label('rotate along the secondary layer of the cube', 200, 240),
                Label('(basically the layer not touching the axis of rotation)', 200, 270),
                Label('Pressing space will toggle the camera y position', 200, 300),
                Label("Drag the mouse to orbit around the rubix's y-axis", 200, 330)
            )
        );
        
        if(Mouse.down and screen.children[1].hits(*Mouse.pos())):
            Program.screen_i = 0;
            screen.visible = False;
    
    def update_game():
        Program.rubix.update();
        Program.render(Program.game_objs);
        screen = Group(
            Group(
                Rect(20, 345, 60, 30, fill='lightGrey'),
                Label('Home', 50, 360),
            ),
            Group(
                Rect(240, 345, 60, 30, fill='lightGrey'),
                Label('Shuffle', 270, 360)
            ),
            Group(
                Rect(320, 345, 60, 30, fill='lightGrey'),
                Label('Solve', 350, 360)
            ),
            Group(
                Rect(10, 10, 100, 70, fill='lightGrey', opacity=60),
                Label('red=x-axis    ', 60, 20, size=15, opacity=80),
                Label('green=y-axis', 60, 40, size=15, opacity=80),
                Label('blue=z-axis  ', 60, 60, size=15, opacity=80)
            )
        );
        if(Mouse.down and Mouse.down_time == 1):
            if(screen.children[0].hits(*Mouse.pos())):
                Program.screen_i = 0;
                screen.visible = False;
                Program.button_pressed = True;
            elif(screen.children[1].hits(*Mouse.pos())):
                Program.rubix.shuffle();
                Program.button_pressed = True;
            elif(screen.children[2].hits(*Mouse.pos())):
                Program.rubix = Rubix.create_rubix(2);
                Program.game_objs = [*Program.rubix.cubie_list(), Program.x_axis, Program.y_axis, Program.z_axis];
                Program.button_pressed = True;
            
    def check_input_action():
        # mouse movement
        Mouse.move_time += 1;
        if(Mouse.down and not Program.button_pressed):
        #if(Mouse.down and Program.mouse_movement):
            if((Mouse.cur_pos.y <= 200 and Program.camera.pos.y <= 0) or (Mouse.cur_pos.y >= 200 and Program.camera.pos.y >= 0)):
                Program.camera.orbit_origin(Mouse.cur_pos - Mouse.prev_pos);
            else:
                Program.camera.orbit_origin(Mouse.prev_pos - Mouse.cur_pos);
        
        
        # keyboard action
        layer = 1;
        if(Keyboard.contains('i') or Keyboard.contains('I')):
            layer = 0;
                
        for key in Keyboard.keys:
            
            """
            # checking keyboard movement
            if(not Program.mouse_movement):
                # movement listeners
                if(key.char == 'w'):
                    Program.camera.pitch += Program.camera.rotate_speed;
                if(key.char == 's'):
                    Program.camera.pitch -= Program.camera.rotate_speed;
                if(key.char == 'a'):
                    Program.camera.yaw -= Program.camera.rotate_speed;
                if(key.char == 'd'):
                    Program.camera.yaw += Program.camera.rotate_speed;
                if(key.char == 'W'):
                    Program.camera.pos += Program.camera.dir * Program.camera.translate_speed;
                if(key.char == 'S'):
                    Program.camera.pos -= Program.camera.dir * Program.camera.translate_speed;
                if(key.char == 'up'):
                    Program.camera.pos.y -= Program.camera.translate_speed;
                if(key.char == 'down'):
                    Program.camera.pos.y += Program.camera.translate_speed;
                if(key.char == 'left'):
                    Program.camera.pos -= LinAlg.cross_prod(Program.camera.dir, V3(0, 1, 0)) * Program.camera.translate_speed;
                if(key.char == 'right'):
                    Program.camera.pos += LinAlg.cross_prod(Program.camera.dir, V3(0, 1, 0)) * Program.camera.translate_speed;
            """
            # checking mouse movement
            if(key.char == 'space'):
                Program.camera.toggle_y();
            
            # rotation listeners
            if(key.down_time == 1):
                if(key.char == 'A'):
                    Program.rubix.cue_rotate('x', 1, layer);
                elif(key.char == 'a'):
                    Program.rubix.cue_rotate('x', -1, layer);
                if(key.char == 's'):
                    Program.rubix.cue_rotate('y', 1, layer);
                elif(key.char == 'S'):
                    Program.rubix.cue_rotate('y', -1, layer);
                if(key.char == 'D'):
                    Program.rubix.cue_rotate('z', 1, layer);
                elif(key.char == 'd'):
                    Program.rubix.cue_rotate('z', -1, layer);
                elif(key.char == '0'):
                    Program.debug = not Program.debug;
        
        # updating previous position
        if(Mouse.move_time == 2):
            Mouse.move_time = 0;
            Mouse.prev_pos = V2(Mouse.cur_pos.x, Mouse.cur_pos.y);
        if(Mouse.down):
            Mouse.down_time += 1;
        else:
            Mouse.up_time += 1;

    def update():
        app.group.clear();
        Keyboard.update_keys();
        Program.check_input_action();
        
        if(Program.screen_i == 0):
            Program.update_home();
        elif(Program.screen_i == 1):
            Program.update_info();
        else:
            Program.update_game();
        
        Program.button_pressed = False;

### event listeners
def onMouseMove(x, y):
    Mouse.set_pos(x, y);
def onMouseDrag(x, y):
    Mouse.set_pos(x, y);
def onMousePress(x, y):
    Mouse.set_init_down(x, y);
def onMouseRelease(x, y):
    Mouse.set_init_up(x, y);

def onKeyHold(keys):
    for new_key in keys:
        contained = False;
        for old_key in Keyboard.keys:
            if(old_key.char == new_key):
                contained = True;
        if(not contained):
            Keyboard.keys.append(Key(new_key));
def onKeyRelease(key):
    for cur_key in Keyboard.keys:
        if(cur_key.char == key):
            Keyboard.keys.remove(cur_key);
            return;

    
### recursive function
def onStep():
    Program.update();
        
