-- Creates a trigger that resets the attribute valid_email only when the email has been changed.
DELIMITER $$
CREATE TRIGGER before_change_email BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email then
        SET NEW.valid_email = 0;
    END IF;
END;
$$
DELIMITER ;
