import math

app.stepsPerSecond = 20;


### class infrastructure

class Color:
    def __init__(self, r=0, g=0, b=0):
        self.r, self.g, self.b = r, g, b;

    def return_rgb(self):
        return rgb(math.floor(self.r), math.floor(self.g), math.floor(self.b));

    def __mul__(self, n):
        return Color(self.r * n, self.g * n, self.b * n);

    def __imul__(self, n):
        self.r *= n;
        self.g *= n;
        self.b *= n;
        return self;

    def __str__(self):
        return f"r: {self.r}, g: {self.g}, b: {self.b}";


class V2:
    def __init__(self, x, y):
        self.x, self.y = x, y;

    def __str__(self):
        return f"2d vector, x: {self.x}, y: {self.y}";


class V3:
    def to_points(coords):
        p = [];
        for i in range(len(coords)):
            if (i % 3 == 0):
                p.append(V3(coords[i], coords[i + 1], coords[i + 2]));
        return p;

    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z;

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}";

    def __add__(self, v):
        return V3(self.x + v.x, self.y + v.y, self.z + v.z);

    def __iadd_(self, v):
        self.x += v.x;
        self.y += v.y;
        self.z += v.z;
        return self;

    def __sub__(self, v):
        return V3(self.x - v.x, self.y - v.y, self.z - v.z);

    def __rsub__(self, v):
        return V3(v.x - self.x, v.y - self.y, v.z - self.z);

    def __mul__(self, n):
        return V3(self.x * n, self.y * n, self.z * n);

    def __rmul__(self, n):
        return V3(self.x * n, self.y * n, self.z * n);

    def __imul__(self, n):
        self.x *= n;
        self.y *= n;
        self.z *= n;
        return self;

    def __truediv__(self, n):
        return V3(self.x / n, self.y / n, self.z / n);

    def __itruediv__(self, n):
        self.x /= n;
        self.y /= n;
        self.z /= n;
        return self;


class Triangle:
    def to_tris(points):
        p = [];
        for i in range(len(points)):
            if (not i % 3):
                p.append(Triangle([points[i], points[i + 1], points[i + 2]]));
        return p;

    def __init__(self, p=V3.to_points([0, 0, 0, 0, 0, 0, 0, 0, 0]), color=Color(0, 0, 0)):
        self.p = p
        self.color = color;

    def __str__(self):
        return f"color: {self.color}, p1: {self.p[0]}, p2: {self.p[1]}, p3: {self.p[2]}";


class Face:
    def convert_tris_to_faces(mesh):
        i = 0;
        faces = [];
        while (i < len(mesh.tri)):
            faces.append(Face(mesh.tri[i], mesh.tri[i + 1]));
            i += 2;
        return faces;

    def __init__(self, tri1, tri2):
        self.tri1 = tri1;
        self.tri2 = tri2;

    def color(self, color):
        self.tri1.color = color;
        self.tri2.color = color;


class Mesh:
    def create_rect(cx, cy, cz, sx=1, sy=1, sz=1):
        rect = Mesh(Triangle.to_tris(V3.to_points([
            # south face
            0, 0, 0, 0, 1, 0, 1, 1, 0,
            0, 0, 0, 1, 1, 0, 1, 0, 0,
            # east face
            1, 0, 0, 1, 1, 0, 1, 1, 1,
            1, 0, 0, 1, 1, 1, 1, 0, 1,
            # north face
            1, 0, 1, 1, 1, 1, 0, 1, 1,
            1, 0, 1, 0, 1, 1, 0, 0, 1,
            # west face
            0, 0, 1, 0, 1, 1, 0, 1, 0,
            0, 0, 1, 0, 1, 0, 0, 0, 0,
            # top face
            0, 1, 0, 0, 1, 1, 1, 1, 1,
            0, 1, 0, 1, 1, 1, 1, 1, 0,
            # bottom face
            0, 0, 0, 1, 0, 0, 1, 0, 1,
            0, 0, 0, 1, 0, 1, 0, 0, 1
        ])));
        rect.translate(cx, cy, cz);
        rect.scale(sx, sy, sz);
        return rect;

    def __init__(self, tris):
        self.tri = tris;

    def translate(self, x, y, z):
        new_tris = [];
        mat_trans = return_mat_trans(x, y, z);
        for tri in self.tri:
            new_tri = Triangle([
                mat_mult(tri.p[0], mat_trans.m),
                mat_mult(tri.p[1], mat_trans.m),
                mat_mult(tri.p[2], mat_trans.m)
            ]);
            new_tris.append(new_tri);
        self.tri = new_tris;

    def scale(self, x, y, z):
        new_tris = [];
        mat_scale = return_mat_scale(x, y, z);
        for tri in self.tri:
            new_tri = Triangle([
                mat_mult(tri.p[0], mat_scale.m),
                mat_mult(tri.p[1], mat_scale.m),
                mat_mult(tri.p[2], mat_scale.m)
            ]);
            new_tris.append(new_tri);
        self.tri = new_tris;

    def __str__(self):
        return f"mesh, tri len: {len(self.tri)}, tri: {self.tri}"


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
        'south': Color(0, 255, 0),  # green
        'east': Color(255, 0, 0),  # red
        'north': Color(0, 0, 255),  # blue
        'west': Color(255, 165, 0),  # orange
        'top': Color(255, 255, 255),  # white
        'bottom': Color(255, 255, 0)  # yellow
    };

    def __init__(self, cx, cy, cz):
        ### need infrastructure in order to pass in and read color information

        # will need system to coordinate color information, rotation, and position with the mesh

        # need mesh from which to render
        self.mesh = Mesh.create_rect(cx, cy, cz);

    def color(self, face, color):
        self.mesh.tri[Cubie.face_codes[face] * 2].color = color;
        self.mesh.tri[Cubie.face_codes[face] * 2 + 1].color = color;


class Rubix:
    def __init__(self, cubes):
        self.cubies = cubes;

    def mesh_list(self):
        l = [];
        for layer in self.cubies:
            for row in layer:
                for cubie in row:
                    l.append(cubie.mesh);
        return l;

    def rotate_y(self, dir, layer):
        pass


class mat4x4:
    def __init__(self, mat=None):
        self.m = mat;


##### below are properties used for rendering #####
### helper functions
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


def draw_tri(tri, col, wire_frame):
    line_col = 'black';
    if (not wire_frame):
        line_col = col.return_rgb();
    Polygon(tri[0].x, tri[0].y, tri[1].x, tri[1].y, tri[2].x, tri[2].y, fill=col.return_rgb(), border=line_col,
            borderWidth=1.2);


def scale_to_screen(v):
    return V3((v.x + 1) / 2 * Program.W, (v.y + 1) / 2 * Program.H, v.z);


def point_at(pos, target, up):
    forw = normalize(target - pos);
    up = normalize(up - dot_prod(forw, up) * forw);
    right = cross_prod(forw, up);
    return mat4x4([
        [right.x, up.x, forw.x, pos.x],
        [right.y, up.y, forw.y, pos.y],
        [right.z, up.z, forw.z, pos.z],
        [0, 0, 0, 1]
    ]);

    ### matrices


def return_mat_trans(x, y, z):
    return mat4x4([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ]);


def return_mat_scale(x, y, z):
    return mat4x4([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ]);


def return_mat_proj(aspect_ratio, FOV_scale, q, z_near):
    return mat4x4([
        [aspect_ratio * FOV_scale, 0, 0, 0],
        [0, FOV_scale, 0, 0],
        [0, 0, q, -z_near * q],
        [0, 0, 1, 1]
    ]);


def return_mat_rx(a):
    return mat4x4([
        [1, 0, 0, 0],
        [0, math.cos(a), -math.sin(a), 0],
        [0, math.sin(a), math.cos(a), 0],
        [0, 0, 0, 1]
    ]);


def return_mat_ry(a):
    return mat4x4([
        [math.cos(a), 0, -math.sin(a), 0],
        [0, 1, 0, 0],
        [math.sin(a), 0, math.cos(a), 0],
        [0, 0, 0, 1]
    ]);


def return_mat_rz(a):
    return mat4x4([
        [math.cos(a), -math.sin(a), 0, 0],
        [math.sin(a), math.cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]);


def mat_quick_inverse(matrix):
    m = matrix.m;
    trans = V3(m[0][3], m[1][3], m[2][3]);
    return mat4x4([
        [m[0][0], m[1][0], m[2][0], dot_prod(-1 * trans, V3(m[0][0], m[1][0], m[2][0]))],
        [m[0][1], m[1][1], m[2][1], dot_prod(-1 * trans, V3(m[0][1], m[1][1], m[2][1]))],
        [m[0][2], m[1][2], m[2][2], dot_prod(-1 * trans, V3(m[0][2], m[1][2], m[2][2]))],
        [0, 0, 0, 1]
    ]);

    ### for clipping purposes


# not needed anymore
def line_plane_intersect(plane_p, plane_n, line_start, line_end):
    n = normalize(plane_n);
    line_dir = line_end - line_start;

    numer = dot_prod(plane_p - line_start, n);
    denom = dot_prod(line_dir, n);

    if (denom == 0):
        raise Exception("error in line_plane_intersect; the line given is parellel to the plane given");

    val = numer / denom;

    return line_start + val * line_dir;


def clip_against_plane(plane_p, plane_n, input_tri):
    plane_n = normalize(plane_n);

    def dist(p):
        return dot_prod(p - plane_p, plane_n);

    inside_points = [];
    outside_points = [];

    d0 = dist(input_tri.p[0]);
    d1 = dist(input_tri.p[1]);
    d2 = dist(input_tri.p[2]);

    if (d0 >= 0):
        inside_points.append(input_tri.p[0]);
    else:
        outside_points.append(input_tri.p[0]);

    if (d1 >= 0):
        inside_points.append(input_tri.p[1]);
    else:
        outside_points.append(input_tri.p[1]);

    if (d2 >= 0):
        inside_points.append(input_tri.p[2]);
    else:
        outside_points.append(input_tri.p[2]);

    if (len(inside_points) == 0):
        return [];
    if (len(inside_points) == 3):
        return [input_tri];

    if (len(inside_points) == 1 and len(outside_points) == 2):
        output_tri1 = Triangle([
            inside_points[0],
            line_plane_intersect(plane_p, plane_n, inside_points[0], outside_points[0]),
            line_plane_intersect(plane_p, plane_n, inside_points[0], outside_points[1])
        ]);

        return [output_tri1];

    if (len(inside_points) == 2 and len(outside_points) == 1):
        output_tri1 = Triangle([
            inside_points[0],
            line_plane_intersect(plane_p, plane_n, inside_points[0], outside_points[0]),
            line_plane_intersect(plane_p, plane_n, inside_points[1], outside_points[0])
        ]);

        output_tri2 = Triangle([
            inside_points[1],
            inside_points[0],
            output_tri1.p[2]
        ]);

        return [output_tri1, output_tri2];

    raise Exception("something went horribly wrong in your clipping function")


def create_rubix(n):
    rubix = [];

    for i in range(n):

        layer = [];

        for j in range(n):

            row = [];

            for k in range(n):

                cubie = Cubie(j - n / 2, i - n / 2, k - n / 2);

                # coloring cubie
                if (i == n - 1):
                    cubie.color('bottom', Cubie.color_codes['bottom']);
                elif (i == 0):
                    cubie.color('top', Cubie.color_codes['top']);

                if (j == n - 1):
                    cubie.color('west', Cubie.color_codes['west']);
                elif (j == 0):
                    cubie.color('east', Cubie.color_codes['east']);

                if (k == 0):
                    cubie.color('south', Cubie.color_codes['south']);
                elif (k == n - 1):
                    cubie.color('north', Cubie.color_codes['north']);

                row.append(cubie);

            layer.append(row);

        rubix.append(layer);

    return Rubix(rubix);


class Program:
    # general properties
    debug = True;

    # projection properties
    W = 400;
    H = 400;
    aspect_ratio = H / W;
    FOV = math.pi / 2 - 1
    FOV_scale = 1 / math.tan(FOV / 2);

    # z scaling
    z_far = 1000;
    z_near = 0.1;
    q = z_far / (z_far - z_near);
    mat_proj = return_mat_proj(aspect_ratio, FOV_scale, q, z_near);

    # camera properties
    camera = V3(0, 0, -4);
    camera_dir = V3(0, 0, 1);
    yaw = 0;
    pitch = 0;

    light_dir = camera_dir;

    rubix = create_rubix(2);
    rubix.rotate_y(0, 1);

    objs = rubix.mesh_list();

    # app.paused = True;
    def render():

        app.group.clear();
        # setting up camera info
        up = V3(0, 1, 0);
        init_dir = V3(0, 0, 1);

        mat_camera_rot_y = return_mat_ry(Program.yaw);
        mat_camera_rot_x = return_mat_rx(Program.pitch);

        Program.camera_dir = normalize(mat_mult(mat_mult(init_dir, mat_camera_rot_x.m), mat_camera_rot_y.m));
        target = Program.camera + Program.camera_dir;
        mat_camera = point_at(Program.camera, target, up);

        Program.light_dir = -1 * Program.camera_dir;

        mat_view = mat_quick_inverse(mat_camera);

        tris_to_raster = [];

        for obj in Program.objs:

            for tri in obj.tri:

                tri_trans, tri_view, tri_proj, tri_scaled = tri, Triangle(), Triangle(), Triangle();

                # creating normalized normal
                line1 = tri_trans.p[1] - tri_trans.p[0];
                line2 = tri_trans.p[2] - tri_trans.p[1];

                normal = normalize(cross_prod(line1, line2));

                # testing if triangle is visible; only then would you want to perform more calculations
                if (dot_prod(normal, tri_trans.p[1] - Program.camera) < 0.1):

                    # converting to camera view (world space -> view space)
                    tri_view.p[0] = mat_mult(tri_trans.p[0], mat_view.m);
                    tri_view.p[1] = mat_mult(tri_trans.p[1], mat_view.m);
                    tri_view.p[2] = mat_mult(tri_trans.p[2], mat_view.m);

                    ### clipping; probably excluding from program
                    """
                    plane_p = V3(0, 0, 1);
                    plane_n = V3(0, 0, 1);

                    tris_clipped = clip_against_plane(plane_p, plane_n, tri_view);
                    """
                    tris_clipped = [tri_view];

                    for tri_clipped in tris_clipped:
                        # projecting on screen
                        tri_proj.p[0] = mat_mult(tri_clipped.p[0], Program.mat_proj.m);
                        tri_proj.p[0] /= tri_proj.p[0].w;
                        tri_proj.p[1] = mat_mult(tri_clipped.p[1], Program.mat_proj.m);
                        tri_proj.p[1] /= tri_proj.p[1].w;
                        tri_proj.p[2] = mat_mult(tri_clipped.p[2], Program.mat_proj.m);
                        tri_proj.p[2] /= tri_proj.p[2].w;

                        # scaling to screen
                        tri_scaled.p[0] = scale_to_screen(tri_proj.p[0]);
                        tri_scaled.p[1] = scale_to_screen(tri_proj.p[1]);
                        tri_scaled.p[2] = scale_to_screen(tri_proj.p[2]);

                        # really janky lighting effect
                        val = (dot_prod(normal, Program.light_dir) + 1) / 2;
                        tri_col = tri.color * val;

                        # for some reason appending this way preserves data, doing it other way doesnt
                        tris_to_raster.append(Triangle([tri_scaled.p[0], tri_scaled.p[1], tri_scaled.p[2]], tri_col));

        # triangles already projected onto camera view so z distance correctly compares depth in sorting

        if (not len(tris_to_raster)):
            return;

        sorted_tris_to_raster = [tris_to_raster[0]];
        for i in range(1, len(tris_to_raster)):

            cur_z = (tris_to_raster[i].p[0].z + tris_to_raster[i].p[1].z + tris_to_raster[i].p[2].z) / 3;

            j = 0;
            appended = False;
            while (j < len(sorted_tris_to_raster) and not appended):

                sorted_z = (sorted_tris_to_raster[j].p[0].z + sorted_tris_to_raster[j].p[1].z +
                            sorted_tris_to_raster[j].p[2].z) / 3;

                if (cur_z > sorted_z):
                    sorted_tris_to_raster.insert(j, tris_to_raster[i]);
                    appended = True;
                j += 1;
            if (not appended):
                sorted_tris_to_raster.append(tris_to_raster[i]);

        for sorted_tri in sorted_tris_to_raster:

            cue = [sorted_tri];

            """
            tris_to_add = 1;
            for i in range(4):
                tris_to_add = len(cue);
                while(tris_to_add > 0):
                    tri = cue.pop(0);
                    tris_to_add -= 1;

                    clipped = [];
                    if(i == 0):
                        clipped = clip_against_plane(V3(0, 0, 0), V3(1, 0, 0), tri);
                    elif(i == 1):
                        clipped = clip_against_plane(V3(0, 0, 0), V3(0, 1, 0), tri);
                    elif(i == 2):
                        clipped = clip_against_plane(V3(Program.W-1, 0, 0), V3(-1, 0, 0), tri);
                    elif(i == 3):
                        clipped = clip_against_plane(V3(0, Program.H-1, 0), V3(0, -1, 0), tri);

                    for clipped_tri in clipped:
                        cue.append(clipped_tri);
            """

            # drawing clipped triangles
            for tri in cue:
                draw_tri(tri.p, sorted_tri.color, Program.debug);

        if (Program.debug):
            for tri in sorted_tris_to_raster:
                Circle(tri.p[0].x, tri.p[0].y, 5, fill='orange');
                Circle(tri.p[1].x, tri.p[1].y, 5, fill='orange');
                Circle(tri.p[2].x, tri.p[2].y, 5, fill='orange');


### event listeners
def onKeyHold(keys):
    if ('w' in keys):
        Program.pitch += 0.03;
    if ('s' in keys):
        Program.pitch -= 0.03;
    if ('a' in keys):
        Program.yaw -= 0.03;
    if ('d' in keys):
        Program.yaw += 0.03;
    if ('i' in keys):
        Program.camera += Program.camera_dir * 0.1;
    if ('k' in keys):
        Program.camera -= Program.camera_dir * 0.1;
    if ('up' in keys):
        Program.camera.y -= 0.1;
    if ('down' in keys):
        Program.camera.y += 0.1;
    if ('left' in keys):
        Program.camera -= cross_prod(Program.camera_dir, V3(0, 1, 0)) * 0.1;
    if ('right' in keys):
        Program.camera += cross_prod(Program.camera_dir, V3(0, 1, 0)) * 0.1;


### recursive function
def onStep():
    Program.render();
    pass

