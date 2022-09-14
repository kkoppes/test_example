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


def moment_x_reference_markdown(
    moment_x_p: float,
    force_y: float,
    force_z: float,
    z_coord_p: float,
    y_coord_p: float,
) -> str:
    """
    Create markdown in LaTeX for moment_x_reference
    args:
        m_moment_x_px_p(float): moment of the force
                                about the point of application in the x direction
        force_y(float): force in the y direction
        force_z(float): force in the z direction
        z_coord_p(float): z coordinate of the point of application of the force
        y_coord_p(float): y coordinate of the point of application of the force
    returns:
        markdown(str): markdown in LaTeX for moment_x_reference
    """

    moment_x_ref = moment_x_reference(
        moment_x_p, force_y, force_z, z_coord_p, y_coord_p
    )
    # for LaTeX
    # pylint: disable=anomalous-backslash-in-string
    markdown_formula = """$$
    M_{xU} = M_{xP} - F_{y}\cdot z_{P} + F_{z}\cdot y_{P}
    $$
    """

    markdown_filled = (f"$${moment_x_ref} = "
    f"{moment_x_p} - {force_y} \cdot {z_coord_p} + {force_z} \cdot {y_coord_p}$$")
    # pylint: enable=anomalous-backslash-in-string
    return markdown_formula, markdown_filled


def moment_y_reference(
    moment_y_p: float,
    force_x: float,
    force_z: float,
    x_coord_p: float,
    z_coord_p: float,
) -> float:
    """
    Calculates the moment of the force about the point of application in the y direction.
    args:
        moment_y_p(float): moment of the force
                                about the point of application in the y direction
        force_x(float): force in the x direction
        force_z(float): force in the z direction
        x_coord_p(float): x coordinate of the point of application of the force
        z_coord_p(float): z coordinate of the point of application of the force
    returns:
        moment_myu(float): moment of the force about the point of application in the y direction
    """

    moment_y_ref = moment_y_p - force_x * z_coord_p + force_z * x_coord_p
    return float(moment_y_ref)
