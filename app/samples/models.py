from sqlalchemy import ForeignKey, Text, Float, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from app.database import Base, str_uniq, int_pk, str_null_true


# Sample Table Model
class Sample(Base):
    __tablename__ = "sample"
    
    sample_name: Mapped[str_uniq] = mapped_column(String, primary_key=True)
    ore_zone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    drill_hole: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    depth_m: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rock_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    geological_complex: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Renamed from "complex"
    code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    texture: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    structure: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    macro_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    micro_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ore_mineralization: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    mineral_compositions: Mapped["MineralComposition"] = relationship("MineralComposition", back_populates="sample")
    ore_mineralizations: Mapped["OreMineralization"] = relationship("OreMineralization", back_populates="sample")
    veins: Mapped["Vein"] = relationship("Vein", back_populates="sample")
    metasomatites: Mapped["Metasomatite"] = relationship("Metasomatite", back_populates="sample")
    rare_ore_minerals: Mapped["RareOreMineralization"] = relationship("RareOreMineralization", back_populates="sample")
    accessory_minerals: Mapped["AccessoryMineral"] = relationship("AccessoryMineral", back_populates="sample")
    photos: Mapped["Photos"] = relationship("Photos", back_populates="sample", uselist=False)

    def __str__(self):
        return (f"{self.__class__.__name__}(sample_name={self.sample_name!r}, "
                f"rock_type={self.rock_type!r}, geological_complex={self.geological_complex!r})")

    def __repr__(self):
        return str(self)


class Photos(Base):
    __tablename__ = "photos"
    
    id: Mapped[int_pk]
    sample_name: Mapped[str] = mapped_column(ForeignKey("sample.sample_name"), nullable=False)
    macro: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    straight_light: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reflected_light: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    sample: Mapped["Sample"] = relationship("Sample", back_populates="photos")

    def __str__(self):
        return (f"{self.__class__.__name__}(sample_name={self.sample_name!r}, "
                f"macro={self.macro!r}, straight_light={self.straight_light!r}, reflected_light={self.reflected_light!r})")

    def __repr__(self):
        return str(self)


# Mineral Composition Table Model
class MineralComposition(Base):
    __tablename__ = "mineral_composition"

    id: Mapped[int_pk]
    sample_name: Mapped[str] = mapped_column(ForeignKey("sample.sample_name"), nullable=False)
    mineral_name: Mapped[str]
    percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    main_secondary: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    sample: Mapped["Sample"] = relationship("Sample", back_populates="mineral_compositions")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, sample_name={self.sample_name!r}, "
                f"mineral_name={self.mineral_name!r}, percentage={self.percentage!r})")

    def __repr__(self):
        return str(self)


# Ore Mineralization Table Model
class OreMineralization(Base):
    __tablename__ = "ore_mineralization"

    id: Mapped[int_pk]
    sample_name: Mapped[str] = mapped_column(ForeignKey("sample.sample_name"), nullable=False)
    mineral_name: Mapped[str]
    percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    main_secondary: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    sample: Mapped["Sample"] = relationship("Sample", back_populates="ore_mineralizations")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, sample_name={self.sample_name!r}, "
                f"mineral_name={self.mineral_name!r}, percentage={self.percentage!r})")

    def __repr__(self):
        return str(self)


# Veins Table Model
class Vein(Base):
    __tablename__ = "veins"

    id: Mapped[int_pk]
    sample_name: Mapped[str] = mapped_column(ForeignKey("sample.sample_name"), nullable=False)
    vein_name: Mapped[str]
    percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    sample: Mapped["Sample"] = relationship("Sample", back_populates="veins")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, sample_name={self.sample_name!r}, "
                f"vein_name={self.vein_name!r}, percentage={self.percentage!r})")

    def __repr__(self):
        return str(self)


# Metasomatites Table Model
class Metasomatite(Base):
    __tablename__ = "metasomatites"

    id: Mapped[int_pk]
    sample_name: Mapped[str] = mapped_column(ForeignKey("sample.sample_name"), nullable=False)
    metasomatite_type: Mapped[str]
    percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    sample: Mapped["Sample"] = relationship("Sample", back_populates="metasomatites")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, sample_name={self.sample_name!r}, "
                f"metasomatite_type={self.metasomatite_type!r}, percentage={self.percentage!r})")

    def __repr__(self):
        return str(self)


# Rare Ore Mineralization Table Model
class RareOreMineralization(Base):
    __tablename__ = "rare_ore_mineralization"

    id: Mapped[int_pk]
    sample_name: Mapped[str] = mapped_column(ForeignKey("sample.sample_name"), nullable=False)
    rare_ore_mineral: Mapped[str]

    sample: Mapped["Sample"] = relationship("Sample", back_populates="rare_ore_minerals")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, sample_name={self.sample_name!r}, "
                f"rare_ore_mineral={self.rare_ore_mineral!r})")

    def __repr__(self):
        return str(self)


# Accessory Minerals Table Model
class AccessoryMineral(Base):
    __tablename__ = "accessory_minerals"

    id: Mapped[int_pk]
    sample_name: Mapped[str] = mapped_column(ForeignKey("sample.sample_name"), nullable=False)
    accessory_mineral: Mapped[str]

    sample: Mapped["Sample"] = relationship("Sample", back_populates="accessory_minerals")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, sample_name={self.sample_name!r}, "
                f"accessory_mineral={self.accessory_mineral!r})")

    def __repr__(self):
        return str(self)
