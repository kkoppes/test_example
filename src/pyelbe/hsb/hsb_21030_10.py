"""module for HSB method 21030-01"""


def moment_x_reference(
    moment_x_p: float,
    force_y: float,
    force_z: float,
    z_coord_p: float,
    y_coord_p: float,
) -> float:
    """
    Calculates the moment of the force about the point of application in the x direction.
    args:
        m_moment_x_px_p(float): moment of the force
                                about the point of application in the x direction
        force_y(float): force in the y direction
        force_z(float): force in the z direction
        z_coord_p(float): z coordinate of the point of application of the force
        y_coord_p(float): y coordinate of the point of application of the force
    returns:
        moment_mxu(float): moment of the force about the point of application in the x direction
    """

    moment_x_ref = moment_x_p - force_y * z_coord_p + force_z * y_coord_p
    return float(moment_x_ref)
