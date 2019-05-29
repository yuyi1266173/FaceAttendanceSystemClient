# !python 3.6
# -*-coding: utf-8 -*-

import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, FLOAT, Boolean, TIMESTAMP

from config import DB_DATA_PATH, LOG, DEFAULT_TIME


engine = create_engine('sqlite:///%s?check_same_thread=False' % DB_DATA_PATH, echo=False)
Base = declarative_base()
db_session = sessionmaker(bind=engine)


def init_data_database():
    ret = False
    try:
        # TODO: create database file
        if os.path.isfile(DB_DATA_PATH) is False:
            Base.metadata.create_all(engine)
    except Exception as e:
        LOG.error("init data database %s" % str(e))
        return ret
    ret = True
    return ret


# 员工信息
class Staff(Base):
    """        员工数据
    ------------------------------------------------------
    id            :   主键，索引
    staff_no      :   工号
    name          :   姓名
    sex           :   性别      0 : 男 default   1：女
    age           :   年龄
    id_card_num   :   身份证号
    department    :   部门
    position      :   职位
    is_collect_face_image : 是否已采集人脸
    face_image_url:   人脸图片存放路径
    entry_time    :   入职时间
    departure_time:   离职时间
    create_time   :   注册时间
    update_time   :   更新时间
    is_delete     :   是否删除
    -----------------------------------------------------
    """

    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    staff_no = Column(Integer)
    name = Column(String)
    sex = Column(Integer, default=0)
    age = Column(Integer, default=0)
    id_card_num = Column(String, default="")
    department = Column(String, default="")
    position = Column(String, default="")
    is_collect_face_image = Column(Boolean, default=False)
    face_image_url = Column(String, default="")
    entry_time = Column(FLOAT, default=DEFAULT_TIME)
    departure_time = Column(FLOAT, default=DEFAULT_TIME)
    create_time = Column(FLOAT, default=DEFAULT_TIME)
    update_time = Column(FLOAT, default=DEFAULT_TIME)
    is_delete = Column(Boolean, default=False)

    @staticmethod
    def add_staff(staff_no, name, **kwargs):
        session = db_session()

        try:
            staffs = session.query(Staff).filter_by(staff_no=staff_no, is_delete=False).all()
        except Exception as e:
            LOG.error("add_staff error: {}".format(e))
            return False, "add_staff error: {}".format(e)

        LOG.info("staffs:{}".format(staffs))

        if len(staffs) > 0:
            LOG.error("staff_no 与已有数据冲突")
            return False, "staff_no 与已有数据冲突"

        data_dict = {
            'staff_no': staff_no,
            'name': name,
        }

        staff_sex = kwargs.get('sex', None)
        if staff_sex is not None:
            data_dict['sex'] = staff_sex

        staff_age = kwargs.get('age', None)
        if staff_age is not None:
            data_dict['age'] = staff_age

        staff_id_card_num = kwargs.get('id_card_num', None)
        if staff_id_card_num is not None:
            data_dict['id_card_num'] = staff_id_card_num

        staff_department = kwargs.get('department', None)
        if staff_department is not None:
            data_dict['department'] = staff_department

        staff_position = kwargs.get('position', None)
        if staff_position is not None:
            data_dict['position'] = staff_position

        staff_face_image_url = kwargs.get('face_image_url', None)
        if staff_face_image_url is not None:
            data_dict['face_image_url'] = staff_face_image_url

        staff_entry_time = kwargs.get('entry_time', None)
        if staff_entry_time is not None:
            data_dict['entry_time'] = staff_entry_time

        staff_departure_time = kwargs.get('departure_time', None)
        if staff_departure_time is not None:
            data_dict['departure_time'] = staff_departure_time

        LOG.info("-----{}".format(data_dict))

        staff = Staff(**data_dict)

        try:
            session.add(staff)
            session.commit()
            ret = staff.staff_no
        except Exception as e:
            LOG.error("add staff to db error:{}".format(e))
            session.rollback()
            session.close()
            ret = False, "add staff to db error:{}".format(e)
        finally:
            session.close()

        LOG.info("return {}".format(ret))
        return ret, None

    @staticmethod
    def update_is_collect_face_image(staff_no, is_collect_face_image):
        ret = False
        session = db_session()

        try:
            staff = session.query(Staff).filter_by(staff_no=staff_no, is_delete=False).first()
            if staff is None:
                LOG.error("数据库中没有对应工号为{}的员工".format(staff_no))
                return ret

            staff.is_collect_face_image = is_collect_face_image
            session.commit()
            ret = staff.staff_no
        except Exception as e:
            session.rollback()
            LOG.error("update_is_collect_face_image error: {}".format(e))
        finally:
            session.close()

        return ret

    @staticmethod
    def update_staff_face_image_url(staff_no, face_image_url):
        ret = False

        if not os.path.isfile(face_image_url):
            LOG.error("图片不存在: face_image_url={}".format(face_image_url))
            return ret

        session = db_session()
        try:
            staff = session.query(Staff).filter_by(staff_no=staff_no, is_delete=False).first()
            if staff is None:
                LOG.error("数据库中没有对应工号为{}的员工".format(staff_no))
                return ret

            staff.face_image_url = face_image_url
            session.commit()
            ret = staff.staff_no
        except Exception as e:
            session.rollback()
            LOG.error("update_staff_face_image_url error: {}".format(e))
        finally:
            session.close()

        return ret


def add_staff_fun_test():
    staff_no_id = None

    try:
        staff_no_id = Staff.add_staff(1011, "wu yu", sex=0, age=26, department="技术部", position="Python开发工程师",
                                      entry_time=time.time(), )
    except Exception as e:
        print(e)

    print("staff_no_id", staff_no_id)

    if staff_no_id not in [None, False]:
        print("update_staff_face_image_url", Staff.update_staff_face_image_url(staff_no_id, "./rose_logo.png"))

    if staff_no_id not in [None, False]:
        print("update_is_collect_face_image", Staff.update_is_collect_face_image(staff_no_id, True))


if __name__ == "__main__":
    import time

    # os.chdir("../../")
    print(os.getcwd())
    init_data_database()
    add_staff_fun_test()

