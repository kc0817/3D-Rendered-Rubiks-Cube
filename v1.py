import math


### class infrastructure 
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

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z;

    def __str__(self):
        return f"type: 3d vector, x: {self.x}, y: {self.y}, z: {self.z}";

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

    def __truediv__(self, n):
        return V3(self.x / n, self.y / n, self.z / n);

    def __itruediv__(self, n):
        self.x /= n;
        self.y /= n;
        self.z /= n;
        return self;


class Face:
    def to_faces(points):
        f = [];
        for i in range(len(points)):
            if (i % 4 == 0):
                f.append(Face([points[i], points[i + 1], points[i + 2], points[i + 3]]));
        return f;

    def __init__(self, points):
        self.p = points;
        self.col = 'grey'


class Cube:
    def __init__(self, faces):
        self.f = faces;


class mat4x4:
    def __init__(self, mat=None):
        self.m = mat;


### helper functions
def to_vec(n):
    return V3(n, n, n);


def mat_mult(vec, mat):
    v = V3(
        vec.x * mat[0][0] + vec.y * mat[0][1] + vec.z * mat[0][2] + mat[0][3],
        vec.x * mat[1][0] + vec.y * mat[1][1] + vec.z * mat[1][2] + mat[1][3],
        vec.x * mat[2][0] + vec.y * mat[2][1] + vec.z * mat[2][2] + mat[2][3]
    );
    v.w = vec.x * mat[3][0] + vec.y * mat[3][1] + vec.z * mat[3][2] + mat[3][3];
    if (v.w):
        v.x /= v.w;
        v.y /= v.w;
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


def draw_face(face, col='white', line_col='black'):
    # initial drawing code
    """
    Line(face[0].x, face[0].y, face[1].x, face[1].y);
    Line(face[1].x, face[1].y, face[2].x, face[2].y);
    Line(face[2].x, face[2].y, face[3].x, face[3].y);
    Line(face[3].x, face[3].y, face[0].x, face[0].y);
    """

    Polygon(face[0].x, face[0].y, face[1].x, face[1].y, face[2].x, face[2].y, face[3].x, face[3].y, fill=col,
            border=line_col, borderWidth=1.2);


### renderer properties
W = 400;
H = 400;
aspect_ratio = H / W;
FOV = 45;
FOV_scale = 1 / math.tan(FOV / 2);

# z scaling
z_far = 1000;
z_near = 0.1;
q = z_far / (z_far - z_near);

app.t = 0;


### matrices
def return_mat_trans(x, y, z):
    return mat4x4([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ]);


def return_mat_proj():
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


### for projection purposes
mat_proj = return_mat_proj();


def scale_to_screen(v):
    return V2((v.x + 1) / 2 * W, (v.y + 1) / 2 * H);


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


### game objects
class Program:
    camera = V3(0, 0, 0);
    camera_dir = V3(0, 0, 1);
    yaw = 0;

    light_dir = normalize(V3(0, -1, -1));

    cube = Cube(Face.to_faces(V3.to_points([
        # south face
        0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0,
        # east face
        1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1,
        # north face
        1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1,
        # west face
        0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0,
        # top face
        0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0,
        # bottom face
        0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1
    ])));
    cube2 = Cube(Face.to_faces(V3.to_points([
        # south face
        3, 0, 0, 3, 1, 0, 4, 1, 0, 4, 0, 0,
        # east face
        4, 0, 0, 4, 1, 0, 4, 1, 1, 4, 0, 1,
        # north face
        4, 0, 1, 4, 1, 1, 3, 1, 1, 3, 0, 1,
        # west face
        3, 0, 1, 3, 1, 1, 3, 1, 0, 3, 0, 0,
        # top face
        3, 1, 0, 3, 1, 1, 4, 1, 1, 4, 1, 0,
        # bottom face
        3, 0, 0, 4, 0, 0, 4, 0, 1, 3, 0, 1
    ])));
    objs = [cube, cube2];


### main function
def render():
    app.group.clear();

    # defining rotation matrices
    mat_rx = return_mat_rx(app.t);
    mat_ry = return_mat_ry(app.t);
    mat_rz = return_mat_rz(app.t);

    # setting up camera info
    up = V3(0, 1, 0);
    target = V3(0, 0, 1);
    mat_camera_rot = return_mat_ry(Program.yaw);
    Program.camera_dir = normalize(mat_mult(target, mat_camera_rot.m));
    target = Program.camera + Program.camera_dir;
    mat_camera = point_at(Program.camera, target, up);

    mat_view = mat_quick_inverse(mat_camera);

    for obj in Program.objs:

        for f in obj.f:

            # translated f
            face_trans = [];

            # calculating new positions for points
            for op in f.p:
                # rotating
                p_rx = mat_mult(op, mat_rx.m);
                p_ry = mat_mult(p_rx, mat_ry.m);
                p_rz = mat_mult(p_ry, mat_rz.m);

                # translating
                p_trans = mat_mult(p_rz, return_mat_trans(0, 0, 4).m);

                face_trans.append(p_trans);

            # creating normalized normal
            line1 = face_trans[1] - face_trans[0];
            line2 = face_trans[2] - face_trans[1];

            normal = normalize(cross_prod(line1, line2));

            # if you want to draw the normals
            """
            normal_start_proj = scale_to_screen(mat_mult((face_trans[1] + face_trans[3]) / 2, mat_proj.m));
            normal_end_proj = scale_to_screen(mat_mult((face_trans[1] + face_trans[3]) / 2 + normal, mat_proj.m));
            Line(normal_start_proj.x, normal_start_proj.y, normal_end_proj.x, normal_end_proj.y);
            """

            # only perform more calculations if going to be visible
            # if(normal.z <= 0):
            if (dot_prod(normal, face_trans[1] - Program.camera) < 0):

                face_proj = [];

                for p in face_trans:
                    # converting to camera view
                    p_view = mat_mult(p, mat_view.m);

                    # projecting
                    p_proj = scale_to_screen(mat_mult(p_view, mat_proj.m));
                    face_proj.append(p_proj);

                val = (dot_prod(normal, Program.light_dir) + 1) / 2 * 255;
                col = rgb(val, val, val);
                draw_face(face_proj, col);


### event listeners
def onKeyHold(keys):
    if ('w' in keys):
        Program.camera += Program.camera_dir * 0.1;
    if ('s' in keys):
        Program.camera -= Program.camera_dir * 0.1;
    if ('a' in keys):
        Program.yaw -= 0.1;
    if ('d' in keys):
        Program.yaw += 0.1;
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
    render();
    # app.t += 0.05;

